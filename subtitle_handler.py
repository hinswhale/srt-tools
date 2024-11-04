# subtitle_handler.py

import pysrt
import ass
from flask import Flask, request, jsonify, send_file
import os



def read_srt(file_path):
    """读取 SRT 文件并返回字幕内容"""
    subs = pysrt.open(file_path)
    return [(sub.start.to_time(), sub.end.to_time(), sub.text) for sub in subs]

def read_ass(file_path):
    """读取 ASS 文件并返回字幕内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        doc = ass.parse(f)
        return [(event.start, event.end, event.text) for event in doc.events]

def write_srt(file_path, subtitles):
    """将字幕写入 SRT 文件"""
    subs = pysrt.SubRipFile()
    for start, end, text in subtitles:
        subs.append(pysrt.SubRipItem(start=start, end=end, text=text))
    subs.save(file_path)

def write_ass(file_path, subtitles):
    """将字幕写入 ASS 文件"""
    doc = ass.Document()
    for start, end, text in subtitles:
        event = ass.Event(start=start, end=end, text=text)
        doc.events.append(event)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(doc))

def upload_subtitle(file_path):
    """上传字幕文件"""
    # 这里可以添加上传逻辑，例如将文件保存到云存储
    pass

def modify_subtitle(subtitles, modifications):
    """修改字幕内容"""
    for index, (start, end, text) in modifications.items():
        if index < len(subtitles):
            subtitles[index] = (start, end, text)
    return subtitles

def cache_subtitle(subtitles, cache_path):
    """将字幕缓存到本地"""
    with open(cache_path, 'w', encoding='utf-8') as f:
        for start, end, text in subtitles:
            f.write(f"{start},{end},{text}\n")

def download_subtitle(file_path):
    """下载字幕文件"""
    # 这里可以添加下载逻辑，例如从云存储获取文件
    pass
