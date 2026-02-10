import os
import argparse

UTF8_BOM = b'\xef\xbb\xbf'

def convert_to_utf8_bom(file_path, dry_run=True):
    with open(file_path, 'rb') as f:
        data = f.read()

    if data.startswith(UTF8_BOM):
        return False

    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        try:
            text = data.decode('cp1252')
        except UnicodeDecodeError:
            print(f"SKIP (unknown encoding): {file_path}")
            return False

    if dry_run:
        print(f"WOULD CONVERT: {file_path}")
        return True

    with open(file_path, 'wb') as f:
        f.write(UTF8_BOM)
        f.write(text.encode('utf-8'))

    print(f"CONVERTED: {file_path}")
    return True

def check_and_optionally_convert(directory, convert=False):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    if f.read().startswith(UTF8_BOM):
                        continue
                convert_to_utf8_bom(
                    file_path,
                    dry_run=not convert 
                )

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Convert text files to UTF-8 with BOM")
    parser.add_argument("directory", help="Directory to scan for .txt files")
    parser.add_argument("--convert", action="store_true", help="Enable conversion (default: dry-run only)")
    
    args = parser.parse_args()
    
    check_and_optionally_convert(
        args.directory,
        convert=args.convert,
    )
