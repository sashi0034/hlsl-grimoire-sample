import os

TARGET_GUID = "7E02B89F-27AC-45A9-8793-FD68F5FB8266"


def replace_in_file(file_path: str, old_str: str, new_str: str) -> None:
    """
    指定ファイル内の old_str を new_str に置換して上書き保存する。
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        if old_str in content:
            new_content = content.replace(old_str, new_str)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
    except Exception as e:
        print(f"[ERROR] {file_path} の置換中にエラーが発生しました: {e}")


def process_files_in_current_directory():
    """
    カレントディレクトリ以下のファイルを再帰的に走査し、
    TARGET_GUID の末尾4文字をファイル名から抽出した数字のみの末尾4文字に置換する。
    """
    # 置換対象 GUID の先頭部分（末尾6文字を除いた部分）
    guid_prefix = TARGET_GUID[:-6]  # => "7E02B89F-27AC-45A9-8793-FD68F5"
    guid_suffix_original = TARGET_GUID[
        -4:
    ]  # => "8266"（参考用・実際は置換で直接 old_str に使う）

    for root, dirs, files in os.walk("."):
        if ".git" in root:
            continue

        for filename in files:
            if (
                filename.endswith(".py")
                or filename.endswith(".dll")
                or filename.endswith(".DDS")
            ):
                continue

            file_path = os.path.join(root, filename)

            # 拡張子を除いたファイル名
            base_name, ext = os.path.splitext(filename)

            # ファイル名から数字以外を除去
            filtered_name = "".join(ch for ch in base_name if ch.isalnum())

            # 末尾4文字を取得（6文字未満の場合は特殊化）
            if len(filtered_name) < 6:
                filtered_name = "AAAAAA" + filtered_name

            new_suffix = filtered_name[-6:]  # 新たに付与する6文字
            new_suffix = new_suffix.upper()  # 大文字に変換

            # 置換前後の文字列
            old_str = TARGET_GUID
            new_str = guid_prefix + new_suffix

            # ファイル内で置換実行
            print(f"Check: {file_path} ({old_str} -> {new_str})")
            replace_in_file(file_path, old_str, new_str)


def main():
    process_files_in_current_directory()


if __name__ == "__main__":
    main()
