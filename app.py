import streamlit as st
import requests

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="Drug Discovery AI | Medical Agent",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تحسين المظهر باستخدام CSS (التصحيح: unsafe_allow_html)
st.markdown("""
    <style>
    /* تحسين لون الخلفية العام */
    .stApp {
        background-color: #fcfcfc;
    }
    /* تنسيق الأزرار لتكون بلمسة طبية زرقاء */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #0056b3;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #004494;
        border: none;
        color: white;
    }
    /* تنسيق صناديق المعلومات */
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. القائمة الجانبية (Sidebar) - الهوية البصرية وحالة النظام
with st.sidebar:
    # في ملف app.py داخل with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/822/822143.png", width=80) # أيقونة قلب طبي
    st.title("لوحة التحكم")
    st.markdown("---")
    
    st.subheader("🌐 حالة النظام")
    # محاكاة لفحص الاتصال (يمكن تطويرها لاحقاً)
    st.success("● المتصفح متصل")
    st.info("● محرك Llama 3.3 جاهز")
    
    st.markdown("---")
    st.subheader("📚 المصادر المفعلة")
    st.write("✓ Neo4j Graph Database")
    st.write("✓ PubMed Central")
    st.write("✓ Tavily Web Search")
    
    if st.button("🔄 إعادة تعيين الجلسة"):
        st.rerun()

# 4. منطقة العنوان والبحث
st.title("🧬 Drug Discovery RAG Explorer")
st.write("نظام خبير مدعوم بالذكاء الاصطناعي للبحث في التفاعلات الدوائية والأبحاث السريرية.")

# تنظيم الواجهة في أعمدة للبحث
col_input, col_btn = st.columns([4, 1])

with col_input:
    query = st.text_input(
        label="Query Input",
        label_visibility="collapsed",
        placeholder="أدخل اسم الدواء أو الحالة الطبية (مثال: Metformin side effects 2024)...",
    )

with col_btn:
    search_button = st.button("تحليل البيانات")

# 5. معالجة البيانات وعرض النتائج
if search_button:
    if not query:
        st.warning("⚠️ يرجى إدخال سؤال أو اسم دواء للبدء.")
    else:
        # استخدام st.status لتجربة مستخدم تفاعلية
        with st.status("🔍 جاري فحص قواعد البيانات والأبحاث...", expanded=True) as status:
            try:
                # طلب البيانات من FastAPI
                st.write("📡 جارٍ إرسال الاستعلام للمحرك الرئيسي...")
                response = requests.post("http://127.0.0.1:8000/ask", json={"prompt": query}, timeout=100)
                
                if response.status_code == 200:
                    data = response.json()
                    status.update(label="✅ اكتمل التحليل بنجاح!", state="complete", expanded=False)
                    
                    # عرض الإجابة الرئيسية في صندوق مميز
                    st.markdown("### 🤖 التحليل العلمي المستخلص")
                    st.info(data.get("answer", "لا توجد إجابة متاحة."))
                    
                    st.markdown("---")
                    st.markdown("### 📑 الأدلة والمصادر المرجعية")
                    
                    # تنظيم المصادر في تبويبات (Tabs)
                    tab_graph, tab_pubmed, tab_web = st.tabs([
                        "🧬 الروابط الهيكلية (Graph)", 
                        "📖 الأبحاث (PubMed)", 
                        "🌐 تحديثات الويب"
                    ])
                    
                    sources = data.get("sources", {})
                    
                    with tab_graph:
                        st.subheader("بيانات Graph Database")
                        graph_info = sources.get("graph", "لا توجد بيانات مهيكلة لهذا الاستعلام.")
                        st.code(graph_info, language="text")
                        
                    with tab_pubmed:
                        st.subheader("ملخصات الأبحاث من PubMed")
                        pubmed_info = sources.get("local_literature", "لم يتم العثور على أبحاث محلية.")
                        st.markdown(f"> {pubmed_info}")
                        
                    with tab_web:
                        st.subheader("نتائج البحث المباشر (2024-2025)")
                        web_info = sources.get("web_updates", "لا توجد تحديثات ويب حديثة.")
                        st.write(web_info)
                        
                else:
                    status.update(label="❌ فشل في جلب البيانات", state="error")
                    st.error(f"خطأ من السيرفر: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                status.update(label="⚠️ خطأ في الاتصال", state="error")
                st.error("تعذر الاتصال بالسيرفر. تأكد من تشغيل ملف `main.py` أولاً.")
            except Exception as e:
                status.update(label="⚠️ خطأ غير متوقع", state="error")
                st.error(f"حدث خطأ: {str(e)}")

# تذييل الصفحة
st.markdown("---")
st.caption("🔍 ملاحظة: هذا النظام يستخدم تقنيات RAG لدمج البيانات. الإجابات مُولدة آلياً لأغراض بحثية فقط.")