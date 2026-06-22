import os
import gradio as gr
import yt_dlp

def download_any_video(video_url):
    if not video_url.strip():
        raise gr.Error("⚠️ أرجوك ضع رابط الفيديو أولاً يا زعيم!")
    
    # الإعداد الذهبي: تحميل جودة شغال ومدمجة مباشرة لتخطي حماية يوتيوب على سيرفر Render
    ydl_opts = {
        'format': 'best',  # اختيار أفضل جودة جاهزة للصوت والصورة معاً مباشرة
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        print(f"⏳ جاري الفحص وسحب الفيديو من الموقع الخارجي...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            
            if os.path.exists(filename):
                return filename, "✅ تم استخراج وتجهيز الفيديو بنجاح عبر نظام 2Download! حمل الآن 👇"
            else:
                raise Exception("File not found after download")
                
    except Exception as e:
        print(f"[2Download Error Log] {e}")
        raise gr.Error("❌ عذراً يا زعيم، الرابط غير مدعوم، أو الموقع يفرض حماية قوية ضد التنزيل!")

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🛡️ استوديو Med Amine Mokni للتحميل العالمي
        ### 📥 منصة 2Download الذكية لتحميل الفيديوهات من جميع المواقع والمنصات بلمحة بصر ⚡
        """
    )
    with gr.Row():
        with gr.Column(scale=1):
            url_input = gr.Textbox(
                label="🔗 الصق رابط الفيديو هنا (تيك توك، فيسبوك، يوتيوب، إنستا، والمزيد...)", 
                placeholder="https://..."
            )
            download_btn = gr.Button("🚀 ابدأ الاستخراج والتحميل الفوري", variant="primary")
        with gr.Column(scale=1):
            status_output = gr.Textbox(label="📊 حالة السيرفر والطلب", interactive=False)
            video_output = gr.Video(label="🎞️ الفيديو المستخرج (اضغط على النقاط الثلاث للتحميل)")

    download_btn.click(
        fn=download_any_video,
        inputs=[url_input],
        outputs=[video_output, status_output]
    )

if __name__ == "__main__":
    demo.queue()
    server_port = int(os.environ.get("PORT", 8080))
    demo.launch(server_name="0.0.0.0", server_port=server_port)
