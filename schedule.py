
import json
import sys
from datetime import date, datetime, timezone, timedelta
from pathlib import Path


JST = timezone(timedelta(hours=9))


def load_schedule():
    """schedule.json を読み込む"""
    path = Path(__file__).parent / "schedule.json"

    if not path.exists():
        raise FileNotFoundError(
            "schedule.json が見つかりません。同じフォルダに配置してください。"
        )

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def filter_schedule(schedule, target_date):
    """指定日の予定を抽出して時刻順に並べる"""
    result = [
        item for item in schedule
        if item.get("start", "").startswith(target_date)
    ]

    return sorted(result, key=lambda item: item.get("start", ""))


def format_event(item):
    """予定1件を表示用の文字列にする"""
    start = datetime.fromisoformat(item["start"]).strftime("%H:%M")
    end = datetime.fromisoformat(item["end"]).strftime("%H:%M")

    title = item.get("title", "（タイトルなし）")
    location = item.get("location") or "（場所なし）"

    return f"{start}-{end}  {title}  @{location}"


def main():
    if len(sys.argv) >= 2:
        target_date = sys.argv[1]

        try:
            date.fromisoformat(target_date)
        except ValueError:
            print("日付は YYYY-MM-DD の形式で指定してください。")
            return
    else:
        target_date = datetime.now(JST).date().isoformat()

    try:
        schedule = load_schedule()
    except FileNotFoundError as e:
        print(e)
        return
    except (json.JSONDecodeError, OSError) as e:
        print(f"schedule.json の読み込みに失敗しました: {e}")
        return

    events = filter_schedule(schedule, target_date)

    print(f"{target_date} の予定 {len(events)} 件")

    for event in events:
        print(format_event(event))


if __name__ == "__main__":
    main()