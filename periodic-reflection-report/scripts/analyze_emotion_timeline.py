#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from deep_translator import GoogleTranslator
from textblob import TextBlob


@dataclass
class DayEmotion:
    date: str
    sentiment_score: float
    sentiment_label: str
    subjectivity: float
    dominant_emotions: List[str]


def _norm_text(value: str) -> str:
    if not value:
        return ""
    return value.replace("<br>", "\n")


def _chunk_text(text: str, chunk_size: int = 3000) -> List[str]:
    if len(text) <= chunk_size:
        return [text]
    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start = end
    return chunks


def _translate_ja_to_en(text: str, translator: GoogleTranslator) -> str:
    translated_parts: List[str] = []
    for chunk in _chunk_text(text):
        translated_parts.append(translator.translate(chunk))
    return "\n".join(translated_parts)


def _to_label(polarity: float) -> str:
    if polarity >= 0.2:
        return "positive"
    if polarity <= -0.2:
        return "negative"
    return "neutral"


def _to_emotions(polarity: float, subjectivity: float) -> List[str]:
    # TextBlob の極性/主観性を使って感情カテゴリに寄せる。
    if polarity >= 0.45:
        return ["joy", "confidence"] if subjectivity >= 0.45 else ["calm", "confidence"]
    if polarity >= 0.15:
        return ["calm", "confidence"]
    if polarity <= -0.45:
        return ["frustration", "anxiety"] if subjectivity >= 0.45 else ["anxiety", "calm"]
    if polarity <= -0.15:
        return ["anxiety", "calm"]
    return ["calm"]


def analyze_record(record: Dict[str, str], translator: GoogleTranslator) -> DayEmotion:
    date = record.get("date", "")
    joined = "\n".join(
        _norm_text(record.get(k, "")) for k in ("experience", "reflection", "abstraction", "next_action")
    ).strip()

    if not joined:
        return DayEmotion(
            date=date,
            sentiment_score=0.0,
            sentiment_label="neutral",
            subjectivity=0.0,
            dominant_emotions=["calm"],
        )

    try:
        translated = _translate_ja_to_en(joined, translator)
    except Exception:
        # 翻訳失敗時は原文をそのまま解析（結果は中立寄りになりやすい）
        translated = joined

    blob = TextBlob(translated)
    polarity = max(-1.0, min(1.0, float(blob.sentiment.polarity)))
    subjectivity = max(0.0, min(1.0, float(blob.sentiment.subjectivity)))
    label = _to_label(polarity)
    dominant = _to_emotions(polarity, subjectivity)

    return DayEmotion(
        date=date,
        sentiment_score=round(polarity, 3),
        sentiment_label=label,
        subjectivity=round(subjectivity, 3),
        dominant_emotions=dominant,
    )


def summarize(days: List[DayEmotion]) -> Dict[str, object]:
    if not days:
        return {
            "days": 0,
            "average_sentiment": 0.0,
            "average_subjectivity": 0.0,
            "label_counts": {"positive": 0, "neutral": 0, "negative": 0},
            "trend": "insufficient_data",
            "most_common_emotions": [],
        }

    avg = sum(d.sentiment_score for d in days) / len(days)
    avg_subjectivity = sum(d.subjectivity for d in days) / len(days)
    label_counts = {"positive": 0, "neutral": 0, "negative": 0}
    emotion_counts: Dict[str, int] = {}

    for d in days:
        label_counts[d.sentiment_label] += 1
        for e in d.dominant_emotions:
            emotion_counts[e] = emotion_counts.get(e, 0) + 1

    if len(days) >= 4:
        first = sum(d.sentiment_score for d in days[: len(days) // 2]) / max(1, len(days) // 2)
        second = sum(d.sentiment_score for d in days[len(days) // 2 :]) / max(1, len(days) - len(days) // 2)
        delta = second - first
        if delta > 0.12:
            trend = "improving"
        elif delta < -0.12:
            trend = "declining"
        else:
            trend = "stable"
    else:
        trend = "stable"

    common_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:3]

    return {
        "days": len(days),
        "average_sentiment": round(avg, 3),
        "average_subjectivity": round(avg_subjectivity, 3),
        "label_counts": label_counts,
        "trend": trend,
        "most_common_emotions": [{"name": k, "count": v} for k, v in common_emotions],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze emotion timeline from daily reflection records.")
    parser.add_argument("--in", dest="in_path", required=True, help="Input JSON path")
    parser.add_argument("--outdir", default="out", help="Output directory (default: out)")
    args = parser.parse_args()

    in_path = Path(args.in_path)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    payload = json.loads(in_path.read_text(encoding="utf-8"))
    records = payload.get("records", [])
    if not isinstance(records, list):
        raise ValueError("'records' must be a list")

    translator = GoogleTranslator(source="ja", target="en")
    analyzed: List[DayEmotion] = []
    for rec in records:
        if not isinstance(rec, dict):
            continue
        analyzed.append(analyze_record(rec, translator))

    analyzed.sort(key=lambda d: d.date)
    summary = summarize(analyzed)

    out = {
        "summary": summary,
        "timeline": [
            {
                "date": d.date,
                "sentiment_score": d.sentiment_score,
                "sentiment_label": d.sentiment_label,
                "subjectivity": d.subjectivity,
                "dominant_emotions": d.dominant_emotions,
            }
            for d in analyzed
        ],
    }

    out_file = outdir / "emotion_timeline.json"
    out_file.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved: {out_file}")


if __name__ == "__main__":
    main()
