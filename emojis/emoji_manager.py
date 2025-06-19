import os
import re
import json
import csv
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

# Android-safe emoji sets by categories
EMOJI_POOL = [
    # 动物与自然
    "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯",
    "🦁", "🐮", "🐷", "🐸", "🐵", "🦄", "🐔", "🐧", "🐦", "🐤",
    "🐝", "🐞", "🦋", "🐢", "🐍", "🐠", "🐬", "🐳", "🦑", "🦀",
    "🌸", "🌻", "🌹", "🌺", "🌼", "🌷", "🌱", "🌲", "🌳", "🌴",

    # 食物与饮料
    "🍏", "🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🫐",
    "🍈", "🍒", "🍑", "🥭", "🍍", "🥥", "🥝", "🍅", "🍆", "🥑",
    "🥦", "🥬", "🥕", "🌽", "🌶️", "🧄", "🧅", "🥔", "🥚", "🍞",
    "🥐", "🥯", "🥨", "🧀", "🥓", "🍗", "🍖", "🌭", "🍔", "🍟",

    # 活动
    "⚽", "🏀", "🏈", "⚾", "🎾", "🏐", "🏉", "🎱", "🏓", "🏸",
    "🥅", "🏒", "🏑", "🏏", "⛳", "🏹", "🎣", "🤿", "🥊", "🥋",
    "🎯", "🎳", "🪁", "🛹", "🥌", "🛷", "⛷️", "🏂", "🏄‍♂️", "🏊‍♀️",
    "🎮", "🎲", "🧩", "🀄", "♟️", "🃏", "🧗", "🏆", "🥇", "🥈", "🥉",

    # 物体
    "⌚", "📱", "💻", "🖨️", "🕹️", "🎮", "📷", "📸", "📹", "🎥",
    "📺", "📻", "🎙️", "🎚️", "🎛️", "☎️", "📞", "📟", "📠", "🔋",
    "🔌", "💡", "🔦", "🕯️", "🛢️", "💰", "💳", "🗝️", "🔑", "🚪",
    "🔒", "🔓", "🔑", "🔐", "🛡️", "🧲", "⚖️", "🔗", "🧰", "🔧",
    "🔨", "🪓", "⛏️", "🛠️", "🗡️", "⚔️", "🔫", "🏹", "🛏️", "🛋️",

    # 旅行与地点
    "🚗", "🚕", "🚙", "🚌", "🚎", "🏎️", "🚓", "🚑", "🚒", "🚐",
    "🛻", "🚚", "🚛", "🚜", "🏍️", "🛵", "🚲", "🛴", "🚨", "🚔",
    "🚦", "🚧", "🛣️", "🛤️", "✈️", "🛩️", "🚁", "🚀", "🛸", "⛵",
    "🚢", "🛳️", "⛴️", "🚤", "🛥️", "🗽", "🗼", "🏰", "🏯", "🌋",
    "🗻", "🏕️", "🏞️", "🏜️", "🏝️", "🏖️", "🏟️", "🏛️", "🏗️",

    # 人物
    "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇",
    "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘", "😗", "😙", "😚",
    "😋", "😜", "😝", "😛", "🤑", "🤗", "🤩", "🥳", "😎", "🤓",
    "🧐", "😕", "🫠", "😟", "🙁", "☹️", "😮", "😯", "😲", "😳",
    "🥺", "😦", "😧", "😨", "😰", "😥", "😢", "😭", "😱", "😖",
    "😣", "😞", "😓", "😩", "😫", "🥱", "😤", "😡", "😠", "🤬",
    "😈", "👿", "👹", "👺", "💀", "☠️", "👻", "👽", "👾", "🤖",
    "👋", "🤚", "🖐️", "✋", "🖖", "👌", "🤌", "🤏", "✌️", "🤞",
    "🫰", "🤟", "🤘", "🤙", "🫵", "🫶", "👐", "🤲", "🙏", "👏",
    "🫡", "🫥", "🤝", "👍", "👎", "👊", "✊", "👈", "👉", "👆",
    "🖕", "👇", "☝️", "🫳", "🫴", "💪", "🦾", "🦿", "🦵", "🦶",
    "👀", "👁️", "👅", "👄", "🧑", "👦", "👧", "👨", "👩", "🧓",
    "👴", "👵", "🧔", "👱‍♂️", "👱‍♀️", "👨‍🦰", "👩‍🦰", "👨‍🦱", "👩‍🦱",

    # 符号
    "❤️", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍", "💔",
    "❣️", "💕", "💞", "💓", "💗", "💖", "💘", "💝", "💟", "☮️",
    "✝️", "☪️", "🕉️", "☸️", "✡️", "🔯", "🕎", "☯️", "☦️", "🛐",
    "⛎", "♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓",
    "🆗", "🆕", "🆙", "🆒", "🆓", "ℹ️", "🆖", "🆚", "🈁", "🈯",
    "🈚", "🈷️", "🈶", "🈸", "🈴", "🈳", "🈲", "🉐", "🉑", "㊗️", "㊙️",
    "🈹", "🈺", "🈵", "🔞", "💯", "🔢", "🔤", "🔡", "🔠", "🆎", "🅰️", "🅱️", "🅾️", "🅿️",
    "©️", "®️", "™️", "#️⃣", "*️⃣", "0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟",
    "🔔", "🔕", "🎵", "🎶", "💤", "💢", "💬", "💭", "🗯️", "♨️", "💦", "💨", "💫", "🕳️", "💣", "💥", "🚨", "💦",
    "💡", "🔑", "🔒", "🔓", "🔏", "🔐", "🛡️", "🧲", "🔗", "⚖️", "🧰", "🔧", "🔨", "🪓", "⛏️", "🛠️", "🗡️", "⚔️",
    "🔫", "🏹", "🛏️", "🛋️", "🛒", "🧺", "🧻", "🧼", "🪥", "🧽", "🪣", "🧴", "🧷", "🧹", "🪒", "🧯", "🛎️"
]

# Regex pattern for emoji (cover most cases, including ZWJ sequences)
EMOJI_REGEX = re.compile(
    r"("
    r"(?:[\U0001F3FB-\U0001F3FF])|"  # skin tone
    r"(?:[\U0001F9B0-\U0001F9B3])|"  # hair
    r"(?:[\U0001F1E6-\U0001F1FF]{2})|"  # flags
    r"(?:[\U0001F600-\U0001F64F])|"
    r"(?:[\U0001F300-\U0001F5FF])|"
    r"(?:[\U0001F680-\U0001F6FF])|"
    r"(?:[\U0001F700-\U0001F77F])|"
    r"(?:[\U0001F780-\U0001F7FF])|"
    r"(?:[\U0001F800-\U0001F8FF])|"
    r"(?:[\U0001F900-\U0001F9FF])|"
    r"(?:[\U0001FA00-\U0001FA6F])|"
    r"(?:[\U0001FA70-\U0001FAFF])|"
    r"(?:[\u2600-\u26FF])|"
    r"(?:[\u2700-\u27BF])|"
    r"(?:[\u2300-\u23FF])|"
    r"(?:[\u2B05-\u2B07])|"
    r"(?:\u200D)"  # zwj joiner
    r")+",
    re.UNICODE
)

SUPPORTED_EXTS = (".json", ".txt", ".md", ".csv", ".xml", ".html", ".htm")

def extract_emojis(text):
    # Find all emoji/sequence, keeping order, including duplicates
    return [m.group(0) for m in EMOJI_REGEX.finditer(text)]

def find_duplicates(emoji_list):
    # Return a set of emojis that occur more than once
    from collections import Counter
    count = Counter(emoji_list)
    return {em for em, c in count.items() if c > 1}

def build_emoji_replace_map(emoji_list, emoji_pool):
    # Only map duplicate emojis; unique ones stay unchanged
    from collections import Counter, deque

    counter = Counter(emoji_list)
    dups = [em for em in emoji_list if counter[em] > 1]
    seen = set()
    dups_unique = []
    for em in dups:
        if em not in seen:
            dups_unique.append(em)
            seen.add(em)
    pool = deque([e for e in emoji_pool if e not in emoji_list])  # don't use emojis already present
    emoji_map = {}
    for em in dups_unique:
        if not pool:
            pool = deque([e for e in emoji_pool if e not in emoji_list])
        if pool:
            emoji_map[em] = pool.popleft()
    return emoji_map

def replace_duplicate_emojis(text, emoji_map):
    # Only replace duplicates (the 2nd, 3rd, ...) occurrence for each
    # First occurrence stays, others replaced
    matches = list(EMOJI_REGEX.finditer(text))
    new_text = []
    last_idx = 0
    seen = {}
    for m in matches:
        em = m.group(0)
        new_text.append(text[last_idx:m.start()])
        seen.setdefault(em, 0)
        seen[em] += 1
        if em in emoji_map and seen[em] > 1:
            new_text.append(emoji_map[em])
        else:
            new_text.append(em)
        last_idx = m.end()
    new_text.append(text[last_idx:])
    return ''.join(new_text)

def process_json_file(src, dst, emoji_map):
    with open(src, "r", encoding="utf-8") as f:
        data = json.load(f)
    def recursive_replace(obj):
        if isinstance(obj, str):
            return replace_duplicate_emojis(obj, emoji_map)
        elif isinstance(obj, list):
            return [recursive_replace(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: recursive_replace(v) for k, v in obj.items()}
        return obj
    new_data = recursive_replace(data)
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)

def process_csv_file(src, dst, emoji_map):
    with open(src, "r", encoding="utf-8", newline='') as f:
        reader = list(csv.reader(f))
    new_rows = []
    for row in reader:
        new_row = [replace_duplicate_emojis(cell, emoji_map) for cell in row]
        new_rows.append(new_row)
    with open(dst, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

def process_txt_file(src, dst, emoji_map):
    with open(src, "r", encoding="utf-8") as f:
        text = f.read()
    new_text = replace_duplicate_emojis(text, emoji_map)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(new_text)

def process_md_file(src, dst, emoji_map):
    process_txt_file(src, dst, emoji_map)

def process_xml_file(src, dst, emoji_map):
    tree = ET.parse(src)
    root = tree.getroot()
    def recursive_xml(elem):
        if elem.text:
            elem.text = replace_duplicate_emojis(elem.text, emoji_map)
        if elem.tail:
            elem.tail = replace_duplicate_emojis(elem.tail, emoji_map)
        for child in elem:
            recursive_xml(child)
    recursive_xml(root)
    tree.write(dst, encoding="utf-8", xml_declaration=True)

class MyHTMLParser(HTMLParser):
    def __init__(self, emoji_map):
        super().__init__()
        self.emoji_map = emoji_map
        self.result = []
    def handle_starttag(self, tag, attrs):
        attr_str = ''.join([f' {k}="{v}"' for k, v in attrs])
        self.result.append(f"<{tag}{attr_str}>")
    def handle_endtag(self, tag):
        self.result.append(f"</{tag}>")
    def handle_data(self, data):
        self.result.append(replace_duplicate_emojis(data, self.emoji_map))
    def handle_entityref(self, name):
        self.result.append(f"&{name};")
    def handle_charref(self, name):
        self.result.append(f"&#{name};")
    def get_html(self):
        return "".join(self.result)

def process_html_file(src, dst, emoji_map):
    with open(src, "r", encoding="utf-8") as f:
        text = f.read()
    parser = MyHTMLParser(emoji_map)
    parser.feed(text)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(parser.get_html())

def main():
    src_dir = os.path.join(os.path.dirname(__file__))
    output_dir = os.path.join(src_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    files = [f for f in os.listdir(src_dir)
             if os.path.isfile(os.path.join(src_dir, f))
             and f.lower().endswith(SUPPORTED_EXTS)
             and not f.startswith("output")]
    for filename in files:
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(output_dir, filename)
        print(f"Processing {filename}")
        with open(src_path, "r", encoding="utf-8") as f:
            text = f.read()
        emoji_list = extract_emojis(text)
        if not emoji_list:
            print(f"  No emojis found in {filename}, skip.")
            continue
        emoji_map = build_emoji_replace_map(emoji_list, EMOJI_POOL)
        ext = os.path.splitext(filename)[-1].lower()
        if ext == ".json":
            process_json_file(src_path, dst_path, emoji_map)
        elif ext == ".txt":
            process_txt_file(src_path, dst_path, emoji_map)
        elif ext == ".md":
            process_md_file(src_path, dst_path, emoji_map)
        elif ext == ".csv":
            process_csv_file(src_path, dst_path, emoji_map)
        elif ext == ".xml":
            process_xml_file(src_path, dst_path, emoji_map)
        elif ext in (".html", ".htm"):
            process_html_file(src_path, dst_path, emoji_map)
        else:
            print(f"  Unsupported file type: {filename}")

if __name__ == "__main__":
    main()
