import os
import re
import math
from collections import defaultdict
from fastapi import APIRouter, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

router = APIRouter()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

bebeEn = (
    "How do I reset my password?",
    "How can I contact customer support?",
    "How do I process a return?",
    "How do I change my email address?",
    "Where can I view my order history?",
    "How do I delete my account?",
    "What are the available payment methods?",
    "How do I pay for my order?",
    "What are the delivery times?",
    "How long does shipping take?",
    "Where is your store located?",
    "What items do you currently have in stock?",
    "How much does the cost?",
    "How can I use my Store Credit?",
    "How much is the shipping fee?",
    "How can I track my order status?"
)


bebeRu = (
    "Как сбросить пароль?",
    "Как связаться с поддержкой?",
    "Как оформить возврат?",
    "Как изменить email?",
    "Где посмотреть историю заказов?",
    "Как удалить аккаунт?",
    "Способы оплаты",
    "Как оплатить?",
    "Сроки доставки",
    "Сколько ждать доставку?",
    "Где находится магазин?",
    "Какие товары есть в наличии?",
    "Сколько стоит?",
    "Как потратить мой бонусный баланс (Store Credit)?",
    "Сколько стоит доставка?",
    "Как отследить статус текущего заказа?"
)

bebeKz = (
    "Құпия сөзді қалай өзгертуге (қалпына келтіруге) болады?",
    "Қолдау қызметіне қалай хабарласуға болады?",
    "Қайтаруды (возврат) қалай рәсімдеу керек?",
    "Email-ды қалай өзгертуге болады?",
    "Тапсырыстар тарихын қайдан көруге болады?",
    "Аккаунтты қалай өшіреді?",
    "Төлем әдістері қандай?",
    "Қалай төлем жасауға болады?",
    "Жеткізу мерзімі қандай?",
    "Жеткізуді қанша уақыт күту керек?",
    "Дүкен қай жерде орналасқан?",
    "Қоймада қандай тауарлар бар?",
    "қанша тұрады?",
    "Бонустық балансты (Store Credit) қалай жұмсауға болады?",
    "Жеткізу құны қанша?",
    "Ағымдағы тапсырыс мәртебесін қалай бақылауға болады?"
)

FAQ = {
    "commands": "\n".join(bebeEn),
    "How do I reset my password?": "Go to Account → Security → Change Password. A reset link will be sent to your registered email address.",
    "How can I contact customer support?": "You can text us right here in this support chat (HELP) or drop an email at support@myshop.com.",
    "How do I process a return?": "Returns are eligible within 14 days of purchase. Just head over to Account → Recent Orders and select the items you'd like to return.",
    "How do I change my email address?": "You can update your email in your profile settings. Go to Account → Personal Information and click the 'Edit Profile' button.",
    "Where can I view my order history?": "Your complete purchase history and active orders can be found under the 'Recent Orders' section in your Account tab.",
    "How do I delete my account?": "You can do this manually by navigating to Account → Security and clicking the red 'Delete Account' link. Please note that this action is irreversible.",
    "What are the available payment methods?": "We accept Visa and MasterCard via our Secure Payment Gateway, as well as our internal Store Credit balance.",
    "How do I pay for my order?": "Add your items to the Basket, open it, and click the 'Proceed to Checkout' button to complete your secure payment.",
    "What are the delivery times?": "Local delivery takes 1-2 business days. Nationwide shipping takes between 3 to 7 business days.",
    "How long does shipping take?": "Local delivery takes 1-2 business days. Nationwide shipping takes between 3 to 7 business days.",
    "Where is your store located?": "Our MYSHOP retail store is located at 34 Manas Street. Looking forward to your visit!",
    "What items do you currently have in stock?": "Our Store catalog currently features the iPhone 17 Pro, MacBook Air M3, Samsung Galaxy S24 Ultra, and Sony WH-1000XM5 headphones. Live stock availability is also updated on the website.",
    "How much does it cost?": "Tech prices fluctuate in real-time. Please check the 'Store' tab for the most up-to-date pricing!",
    "How can I use my Store Credit?": "Your current Store Credit balance is displayed in your Account dashboard. You can apply these funds directly during the Checkout process.",
    "How much is the shipping fee?": "Most orders and items in your Basket qualify for free courier delivery (Estimated Shipping: Free)!",
    "How can I track my order status?": "Head over to the Account tab. In the 'Recent Orders' table, you will see the live status (e.g., 'Delivered' or 'Processing') next to each of your orders.",
    "командалар": "\n".join(bebeKz),
    "Құпия сөзді қалай өзгертуге (қалпына келтіруге) болады?": "Account → Security → Change Password бөліміне өтіңіз. Өзгертуге арналған сілтеме сіздің email поштаңызға жіберіледі.",
    "Қолдау қызметіне қалай хабарласуға болады?": "Сіз бізге тікелей осы қолдау чатында (HELP) жаза аласыз немесе support@myshop.com поштасына хат жібере аласыз.",
    "Қайтаруды (возврат) қалай рәсімдеу керек?": "Тауарды қайтару 14 күн ішінде жүзеге асырылады. Жеке кабинетке (Account) → Recent Orders бөліміне өтіп, қайтарғыңыз келетін тапсырысты таңдаңыз.",
    "Email-ды қалай өзгертуге болады?": "Поштаны жеке кабинетте өзгертуге болады. Account → Personal Information өтіп, 'Edit Profile' батырмасын басыңыз.",
    "Тапсырыстар тарихын қайдан көруге болады?": "Барлық сатып алу тарихы мен ағымдағы тапсырыстар Account қосымшасындағы 'Recent Orders' модулінде орналасқан.",
    "Аккаунтты қалай өшіреді?": "Мұны өзіңіз істей аласыз. Account → Security бөліміне өтіп, қызыл түсті 'Delete Account' сілтемесін басыңыз. Бұл әрекетті кейін қайтару мүмкін емес.",
    "Төлем әдістері қандай?": "Биз Visa/MasterCard карталарын Secure Payment Gateway арқылы, сондай-ақ дүкеннің ішкі Store Credit балансын қабылдаймыз.",
    "Қалай төлем жасауға болады?": "Тауарларды Basket-ке (Себетке) қосыңыз, оған өтіп, қауіпсіз төлем жасау үшін 'Proceed to Checkout' батырмасын басыңыз.",
    "Жеткізу мерзімі қандай?": "Қала ішінде құрылғыларды жеткізу 1-2 жұмыс күнін алады. Ел бойынша — 3 күннен 7 күнге дейін.",
    "Жеткізуді қанша уақыт күту керек?": "Қала ішінде жеткізу 1-2 жұмыс күнін алады. Ел бойынша — 3 күннен 7 күнге дейін.",
    "Дүкен қай жерде орналасқан?": "Біздің MYSHOP дүкеніміз мына мекенжайда орналасқан: Манас көшесі, 34. Сізді сауда жасауға күтеміз!",
    "Қоймада қандай тауарлар бар?": "Біздің каталогта (Store) келесі тауарлар бар: iPhone 17 Pro, MacBook Air M3, Samsung Galaxy S24 Ultra және Sony WH-1000XM5 құлаққаптары. Қолда бар тауарлардың нақты саны сайтта көрсетілген.",
    "Қанша тұрады ?": "Техника бағасы нақты уақыт режимінде үнемі жаңартылып тұрады. Ағымдағы бағаны 'Store' қосымшасынан тексеріңіз!",
    "Бонустық балансты (Store Credit) қалай жұмсауға болады?": "Сіздің ағымдағы Store Credit балансыңыз Жеке кабинетте (Account) көрсетіледі. Қолжетімді қаражатты тапсырысты рәсімдеу кезінде (Checkout кезеңінде) қолдана аласыз.",
    "Жеткізу құны қанша?": "Себетіңіздегі (Basket) көптеген тапсырыстар мен тауарлар үшін курьерлік жеткізу тегін жүреді (Estimated Shipping: Free)!",
    "Ағымдағы тапсырыс мәртебесін қалай бақылауға болады?": "Account қосымшасына өтіңіз. 'Recent Orders' кестесінде әр тапсырыстың тұсында оның ағымдағы мәртебесі (мысалы, 'Delivered' немесе 'Processing') көрсетілген.",
    "команды": "\n".join(bebeRu),
    "Как сбросить пароль?": "Перейдите в раздел Account → Security → Change Password. Ссылка для изменения будет отправлена на ваш email.",
    "Как связаться с поддержкой?": "Вы можете написать нам прямо здесь, в чате поддержки (HELP), либо отправить письмо на support@myshop.com.",
    "Как оформить возврат?": "Возврат оформляется в течение 14 дней. Перейдите в Личный кабинет (Account) → Recent Orders и выберите нужный заказ для возврата.",
    "Как изменить email?": "Изменить почту можно в личном кабинете. Перейдите в Account → Personal Information → кнопка 'Edit Profile'.",
    "Где посмотреть историю заказов?": "Вся история и текущие покупки находятся на вкладке Account в модуле 'Recent Orders'.",
    "Как удалить аккаунт?": "Вы можете сделать это самостоятельно. Перейдите в Account → Security и нажмите на красную ссылку 'Delete Account'. Действие необратимо.",
    "Способы оплаты": "Мы принимаем карты Visa/MasterCard через Secure Payment Gateway, а также внутренний баланс магазина Store Credit.",
    "Как оплатить?": "Добавьте товары в Basket (Корзину), перейдите в нее и нажмите кнопку 'Proceed to Checkout' для безопасной оплаты.",
    "Сроки доставки": "Доставка девайсов по городу занимает 1-2 рабочих дня. По стране — от 3 до 7 дней.",
    "Сколько ждать доставку?": "Доставка по городу занимает 1-2 рабочих дня. По стране — от 3 до 7 дней.",
    "Где находится магазин?": "Наш магазин MYSHOP расположен по адресу: ул. Манаса, 34. Ждем вас за покупками!",
    "Какие товары есть в наличии?": "В нашем каталоге (Store) представлены: iPhone 17 Pro, MacBook Air M3, Samsung Galaxy S24 Ultra и наушники Sony WH-1000XM5. Актуальное количество штук тоже нв сайте.",
    "Сколько стоит ?": "Цены на технику постоянно обновляются в режиме реального времени. Проверьте актуальную стоимость во вкладке 'Store'!",
    "Как потратить мой бонусный баланс (Store Credit)?": "Ваш текущий баланс Store Credit отображается в Личном кабинете (Account). Вы можете применить доступные средства на этапе оформления заказа в Checkout.",
    "Сколько стоит доставка?": "Для большинства заказов и позиций в вашей корзине (Basket) действует бесплатная курьерская доставка (Estimated Shipping: Free)!",
    "Как отследить статус текущего заказа?": "Зайдите во вкладку Account. В таблице 'Recent Orders' напротив каждого заказа указан его актуальный статус (например, 'Delivered' или 'Processing')."
}

STOP_WORDS = {"how", "where", "what", "when", "why", "who", "which",
    "i", "me", "my", "mine", "you", "your", "yours",
    "in", "on", "at", "to", "for", "with", "from", "by", "about",
    "and", "or", "but", "so", "if", "not", "no", "yes", "this", "that",
    "the", "a", "an", "is", "are", "do", "does", "just", "already", "yet" ,
    "как", "где", "что", "когда", "почему", "зачем", "мне", "я", "мой", "в",
    "на", "с", "по", "из", "для", "и", "или", "а", "но", "не", "это", "то",
    "так", "да", "нет", "ли", "бы", "же", "ещё", "уже","қалай", "қайда", "қайдан",
    "не", "неге", "неліктен", "қашан", "кім", "қанша", "неше","мен", "маған",
    "менің", "сен", "сенің", "сіз", "біз", "ол", "бұл", "сондай","ішінде", "үшін",
    "туралы", "арқылы", "бойынша", "және", "немесе", "бірақ", "да", "де", "та", "те",
    "ма", "ме", "ба", "бе", "па", "пе", "шығар", "ғой", "қой", "қазір", "әлі", "жоқ", "иә"}

def tokenize(text: str) -> list[str]:
    text = text.lower()
    tokens = re.findall(r'[а-яёa-z]+', text)
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 2]

def compute_tf(tokens: list[str]) -> dict:
    tf = defaultdict(int)
    for token in tokens: tf[token] += 1
    total = len(tokens) if tokens else 1
    return {k: v / total for k, v in tf.items()}

def compute_idf(documents: list[list[str]]) -> dict:
    n = len(documents)
    idf = defaultdict(float)
    all_words = set(w for doc in documents for w in doc)
    for word in all_words:
        doc_count = sum(1 for doc in documents if word in doc)
        idf[word] = math.log((n + 1) / (doc_count + 1)) + 1
    return idf

def tfidf_vector(tokens: list[str], idf: dict) -> dict:
    tf = compute_tf(tokens)
    return {word: tf[word] * idf.get(word, 1.0) for word in tokens}

def cosine_similarity(vec1: dict, vec2: dict) -> float:
    common = set(vec1) & set(vec2)
    if not common: return 0.0
    dot = sum(vec1[w] * vec2[w] for w in common)
    norm1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    norm2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
    if norm1 == 0 or norm2 == 0: return 0.0
    return dot / (norm1 * norm2)

class FAQBot:
    def __init__(self, faq: dict, threshold: float = 0.15):
        self.faq = faq
        self.threshold = threshold
        self.questions = list(faq.keys())
        self.answers = list(faq.values())
        self.tokenized = [tokenize(q) for q in self.questions]
        self.idf = compute_idf(self.tokenized)
        self.vectors = [tfidf_vector(tokens, self.idf) for tokens in self.tokenized]

    def respond(self, user_input: str) -> str:
        tokens = tokenize(user_input)
        if not tokens: return "Not understand Question"
        user_vec = tfidf_vector(tokens, self.idf)
        best_score, best_idx = 0.0, -1
        for i, faq_vec in enumerate(self.vectors):
            score = cosine_similarity(user_vec, faq_vec)
            if score > best_score:
                best_score, best_idx = score, i
        if best_score >= self.threshold:
            return f"Answer for question: ''{self.questions[best_idx]}'' - " + self.answers[best_idx]
        return "-------Not found similar question--------"

bot = FAQBot(FAQ)

# ===== API end =====
class ChatRequest(BaseModel):
    message: str

# router
@router.post("/")
async def chat_endpoint(request: ChatRequest, fastapi_req: Request):
    answer = bot.respond(request.message)
    user_ip = fastapi_req.client.host

    try:
        supabase.table("chat_history").insert({
            "message": request.message,
            "response": answer,
            "user_ip": user_ip
        }).execute()
    except Exception as e:
        print(f"error Supabase: {e}")

    return {"response": answer, "your_ip": user_ip}