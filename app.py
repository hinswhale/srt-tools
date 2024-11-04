import pysrt
import ass
from flask import Flask, request, jsonify, send_file,render_template
import os
from subtitle_handler import read_srt, read_ass, write_srt, write_ass, upload_subtitle, modify_subtitle, cache_subtitle, download_subtitle


app = Flask(__name__)

# 确保 uploads 目录存在
upload_folder = 'uploads'
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

@app.route('/', methods=['GET'])
def home():
    """主页，渲染 b.html"""
    return render_template('a.html')

@app.route('/upload', methods=['POST'])
def upload_subtitles():
    """处理中文字幕和英文字幕文件上传"""
    if 'chinese_file' not in request.files or 'english_file' not in request.files:
        return jsonify({'error': '没有文件上传'}), 400

    chinese_file = request.files['chinese_file']
    english_file = request.files['english_file']

    if chinese_file.filename == '' or english_file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400

    if chinese_file and chinese_file.filename.endswith('.srt'):
        chinese_content = chinese_file.read().decode('utf-8')
        # 这里可以添加解析中文字幕的逻辑
    else:
        return jsonify({'error': '只支持 SRT 文件'}), 400

    if english_file and english_file.filename.endswith('.srt'):
        english_content = english_file.read().decode('utf-8')
        # 这里可以添加解析英文字幕的逻辑
    else:
        return jsonify({'error': '只支持 SRT 文件'}), 400

    return jsonify({
        'message': '文件上传成功',
        'chinese_content': chinese_content,
        'english_content': english_content
    }), 200

@app.route('/modify', methods=['POST'])
def modify_subtitle_api():
    """修改字幕内容"""
    data = request.json
    subtitles = data.get('subtitles', [])
    modifications = data.get('modifications', {})
    updated_subtitles = modify_subtitle(subtitles, modifications)
    return jsonify(updated_subtitles), 200

@app.route('/cache', methods=['POST'])
def cache_subtitle_api():
    """将字幕缓存到本地"""
    data = request.json
    subtitles = data.get('subtitles', [])
    cache_path = data.get('cache_path', 'cache.txt')
    cache_subtitle(subtitles, cache_path)
    return jsonify({'message': 'Subtitles cached successfully'}), 200

@app.route('/download/<filename>', methods=['GET'])
def download_subtitle(filename):
    """下载字幕文件"""
    file_path = os.path.join('uploads', filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
