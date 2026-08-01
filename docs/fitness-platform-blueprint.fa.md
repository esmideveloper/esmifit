# سند اجرایی پلتفرم جامع بدنسازی و فیتنس

> نسخه ۱.۰ — طرح محصول، معماری و نقشهٔ راه از صفر تا بهره‌برداری

## 0) فرض‌های تصمیم‌ساز

- محصول یک **SaaS چندسکویی** برای سه نقش «ورزشکار/کاربر»، «مربی» و «ادمین» است؛ موبایل تجربهٔ اصلی ثبت روزانه و وب/دسکتاپ تجربهٔ عمیق‌تر مدیریت و تحلیل است.
- بازار اولیه فارسی‌زبان است، اما هسته از ابتدا i18n، تقویم/واحد قابل تنظیم، و چندارزی طراحی می‌شود. پرداخت پشت یک درگاه انتزاعی قرار می‌گیرد تا بتوان از ارائه‌دهندهٔ محلی یا Stripe استفاده کرد.
- توصیهٔ AI صرفاً آموزشی و ورزشی است؛ تشخیص، درمان، تجویز دارو، رژیم درمانی، یا توصیه برای کاربران پرخطر ممنوع است. کاربر باید تأیید کند که جایگزین پزشک نیست.
- اولویت راهبردی: **اعتماد به داده، تداوم عادت، و برنامهٔ قابل اجرا**؛ نه تولید متن یا نمودار صرف.

---

## 1) تحلیل مسئله و تعریف محصول

### مسئلهٔ اصلی
کاربر برای رسیدن به هدف بدنی (کاهش چربی، عضله‌سازی، افزایش قدرت یا حفظ سلامت) معمولاً با برنامه‌های عمومی، ثبت پراکندهٔ داده‌ها، نبود بازخورد به‌موقع و ارتباط پرهزینه با مربی مواجه است. مربی نیز ابزار یکپارچه‌ای برای ساخت برنامه، مشاهدهٔ پایبندی، اصلاح برنامه و مدیریت پرداخت ندارد. ادمین هم به کنترل محتوا، کیفیت مربیان، سلامت سیستم و داده‌های کسب‌وکار نیاز دارد.

### راه‌حل
یک پلتفرم واحد که داده‌های پروفایل، هدف، محدودیت، تمرین، تغذیه و پیشرفت را جمع می‌کند و از آن برای:
1. اجرای برنامهٔ روزانهٔ روشن و قابل ثبت؛
2. همکاری ساختاریافتهٔ کاربر و مربی؛
3. پیشنهادهای AI **با تأیید/قواعد ایمنی**؛
4. سنجش پایبندی و پیشرفت؛
5. فروش اشتراک و خدمات مربی‌گری؛
استفاده می‌کند.

### شاخص‌های موفقیت اولیه
- Activation: حداقل 60٪ کاربران جدید در 24 ساعت پروفایل، هدف و اولین برنامه را تکمیل کنند.
- Habit: حداقل 35٪ کاربران فعال هفتگی، 3 جلسه در هفته ثبت کنند.
- Adherence: میانگین تکمیل تمرین برنامه‌ریزی‌شده > 65٪ در هفتهٔ چهارم.
- Coach value: زمان ساخت/اصلاح برنامه برای هر ورزشکار < 15 دقیقه.
- Quality: نرخ پیشنهاد AI که توسط کاربر/مربی پذیرفته می‌شود، با کنترل ایمنی و بازخورد سنجیده شود.

### پرسوناها
| نقش | نیاز اصلی | نتیجهٔ مطلوب |
|---|---|---|
| ورزشکار مبتدی | راهنمای ساده و ایمن | «امروز دقیقاً چه کار کنم؟» |
| ورزشکار جدی | پیشرفت قابل اندازه‌گیری | حجم/قدرت/تغذیه و روند قابل تحلیل |
| مربی | مدیریت چند ورزشکار | برنامه‌ریزی، بازخورد، هشدار پایبندی |
| ادمین/اپریشن | رشد و کنترل کیفیت | درآمد، محتوا، تیکت، تخلف و سلامت سرویس |

---

## 2) محدودهٔ MVP: چه بسازیم و چه نسازیم

### MVP (نسخهٔ قابل عرضه)
1. ثبت‌نام، ورود، بازیابی حساب، نقش کاربر/مربی/ادمین.
2. Onboarding: سن، قد، وزن، جنسیت (اختیاری/با رضایت)، سطح تجربه، هدف، تجهیزات، روزهای در دسترس، آسیب/محدودیت و ترجیح غذایی.
3. کتابخانهٔ تمرین و سازندهٔ برنامهٔ ساده؛ برنامهٔ هفتگی، حرکت، ست/تکرار/وزن/RPE، و ثبت تکمیل.
4. برنامهٔ غذایی سطح «کالری و ماکرو + وعده‌های پیشنهادی»؛ نه جایگزین رژیم درمانی.
5. ثبت وزن، اندازه‌ها، عکس پیشرفت با رضایت صریح و نمودار روند.
6. داشبورد امروز، برنامهٔ امروز، streak، پایبندی و روند وزن.
7. پنل مربی: لیست ورزشکاران، ساخت/تخصیص/ویرایش برنامه، یادداشت و مشاهدهٔ پیشرفت.
8. AI Coach محدود و ایمن: پرسش‌وپاسخ مبتنی بر دانش تأییدشده و تولید **پیشنهاد پیش‌نویس** برنامه.
9. اشتراک پایه و پرداخت یک‌باره/دوره‌ای با وب‌هوک idempotent.
10. اعلان push/email برای جلسه، یادآوری ثبت وزن و تمدید اشتراک.
11. پنل ادمین پایه: کاربر، مربی، محتوا، اشتراک، تیکت و audit log.
12. Observability، بکاپ، کنترل دسترسی، تست‌های حیاتی و سیاست حریم خصوصی.

### خارج از MVP (فازهای بعدی)
- اتصال پوشیدنی‌ها (Apple Health, Google Health Connect, Garmin) و همگام‌سازی دوطرفه.
- ویدئوی زنده، بازارگاه مربیان، برنامهٔ گروهی، شبکهٔ اجتماعی و چالش‌های عمومی.
- شمارش کالری با عکس، تشخیص فرم حرکت با ویدئو، تولید ویدئو/آواتار.
- رژیم بالینی، تله‌مدیسین، نسخهٔ دارویی، ژنتیک/آزمایش خون.
- چندمستاجری سازمانی، white-label، کیف پول و سیستم ارجاع پیچیده.

**قاعدهٔ تصمیم:** اگر قابلیت، تکمیل تمرین/ثبت پیشرفت/دریافت ارزش مربی را در چهار هفتهٔ اول بهتر نمی‌کند، به MVP اضافه نشود.

---

## 3) معماری کلان

```text
Mobile (React Native) ─┐
Web / Desktop (Next.js) ├─ CDN/WAF ─ API Gateway / BFF (NestJS)
Admin (Next.js) ───────┘                       │
                                      Modular Monolith (REST/OpenAPI)
              ┌─────────────┬───────────────┬───┼──────┬───────────────┐
              │ Identity    │ Training      │ Nutrition│ Billing       │ Coach/Admin │
              └─────────────┴───────────────┴───┼──────┴───────────────┘
                                                  │
                  PostgreSQL + pgvector | Redis | Object Storage | Queue/Workers
                                                  │
               LLM Gateway + Guardrails + RAG + Tool layer | Analytics/Warehouse
```

### اصل معماری
با **Modular Monolith** شروع شود، نه microservice: تراکنش و توسعه سریع‌تر، هزینهٔ عملیات کمتر و مرزهای دامنه روشن. هر ماژول مالک جدول/API خود است. با رشد، AI worker، Notification worker و Analytics جدا می‌شوند و فقط حوزه‌های پرفشار به سرویس مستقل مهاجرت می‌کنند.

### لایه‌ها
- **Frontend:** BFF-friendly، cache آفلاین برای لاگ تمرین، i18n/RTL، Design System مشترک.
- **Backend:** API نسخه‌دار، OpenAPI، RBAC/ABAC، domain events و outbox برای رخدادهای قابل اتکا.
- **Database:** PostgreSQL منبع حقیقت تراکنشی؛ Redis برای cache، rate limit، session و job کوتاه؛ pgvector ابتدا برای RAG.
- **AI:** سرویس جدا پشت gateway؛ هیچ LLM مستقیماً به DB یا پرداخت دسترسی ندارد.
- **Notification:** رخداد دامنه → Outbox → Queue → worker → provider (FCM/APNs/email/SMS) با preference و quiet hours.
- **File storage:** شیء خصوصی، URL امضاشده، آنتی‌ویروس، تبدیل تصویر، lifecycle policy.
- **Payment:** Billing adapter، invoice/transaction ledger، وب‌هوک امضاشده و idempotent؛ وضعیت پرداخت فقط از وب‌هوک معتبر تغییر کند.
- **Analytics:** event tracking سمت کلاینت/سرور، warehouse جدا از DB عملیاتی؛ PII حداقلی و pseudonymous.

---

## 4) استک پیشنهادی و دلیل انتخاب

| لایه | انتخاب | دلیل |
|---|---|---|
| Mobile | React Native + Expo + TypeScript | یک کدبیس iOS/Android، push/camera آسان، سرعت MVP بالا |
| Web / desktop | Next.js (React, TypeScript) PWA؛ Tauri فقط اگر desktop native لازم شد | پنل و SEO، اشتراک کامپوننت؛ PWA ابتدا هزینه را کم می‌کند |
| UI | Tailwind CSS + shadcn/ui + React Native UI kit + tokens | سرعت، دسترس‌پذیری، سازگاری و تم روشن/تیره |
| Backend | NestJS + TypeScript + Fastify | ماژول‌بندی، validation/guards، OpenAPI و یک زبان در کل محصول |
| ORM/migration | Prisma یا Drizzle + migration بازبینی‌شده | type safety و تغییر schema قابل ردیابی |
| DB | PostgreSQL 16 + pgvector | تراکنش‌های قابل اتکا، JSONB، جست‌وجو و RAG اولیه در یک سرویس |
| Cache/queue | Redis + BullMQ؛ در مقیاس بالا SQS/RabbitMQ | job، retry، rate limit و اعلان قابل اتکا |
| Storage | S3-compatible (AWS S3/Cloudflare R2/MinIO) | خصوصی، مقیاس‌پذیر، URL امضاشده |
| AI | LLM Gateway مستقل، مدل تجاری قابل‌تعویض + model fallback | کنترل هزینه، لاگ، safety و عدم وابستگی به یک vendor |
| Auth | OIDC/OAuth2، JWT کوتاه‌عمر + refresh rotation؛ Auth0/Keycloak یا پیاده‌سازی کنترل‌شده | امنیت و رشد سریع |
| Observability | OpenTelemetry + Sentry + Prometheus/Grafana + Loki | trace، خطا، متریک و لاگ قابل پیگیری |
| Infra | Docker، Terraform، GitHub Actions، Kubernetes/ECS در رشد | محیط تکرارپذیر و استقرار امن |

---

## 5) ماژول‌ها و قرارداد سطح بالا

| ماژول | ورودی‌های اصلی | خروجی | نقش‌ها | وابستگی‌ها |
|---|---|---|---|---|
| Identity | ایمیل/موبایل، رمز/OTP، consent | session/token، حساب تأییدشده | همه | Auth، audit |
| Profile & Goals | مشخصات، هدف، تجهیزات، محدودیت | پروفایل نسخه‌دار، سطح ریسک | User/Coach | Identity, consent |
| Training | برنامه، حرکت، ست/تکرار، لاگ/RPE | برنامهٔ منتشرشده، adherence، PR | User/Coach | Exercise catalog, profile |
| Nutrition | ترجیح، انرژی هدف، وعده/لاگ | target macro، برنامه/روند | User/Coach | Profile, food catalog |
| Progress | وزن، سایز، عکس، حس/خواب | timeline، نمودار، هشدار روند | User/Coach | Storage, analytics |
| AI Coach | سؤال، context مجاز، بازخورد | پاسخ دارای citation، draft/alert | User/Coach | RAG, policy, tools |
| Coach workspace | ورزشکار، template، note، review | assignment، feedback | Coach | Training, progress, billing |
| Admin/CMS | محتوا، نقش، moderation، تنظیم | publish/moderation/audit | Admin | همهٔ ماژول‌ها |
| Billing | plan، checkout، webhook | subscription، invoice، entitlement | User/Admin | Payment provider, notification |
| Notification | preference، event، زمان‌بندی | push/email/SMS delivery | همه | Queue, providers |
| Support | ticket، پیام، attachment | SLA/status/resolution | User/Coach/Admin | Identity, storage |
| Reporting | events و aggregates | KPI و export مجاز | Coach/Admin | warehouse |

### قواعد نقش و مالکیت
- User فقط داده و فایل خود را می‌بیند؛ Coach فقط ورزشکارانی را که assignment فعال دارند؛ Admin دسترسی حداقلی و ثبت‌شده دارد.
- هر تغییر برنامه یک `version` دارد. برنامهٔ تکمیل‌شده هرگز overwrite نمی‌شود؛ برنامهٔ جدید از نسخهٔ بعدی شروع می‌شود.
- Coach می‌تواند draft AI را تأیید/ویرایش کند؛ AI نمی‌تواند بدون policy و رضایت، تغییر اجرایی اعمال کند.

---

## 6) مدل دادهٔ سطح بالا

### هویت و دسترسی
`users`, `user_profiles`, `roles`, `user_roles`, `sessions`, `consents`, `coach_profiles`, `coach_client_assignments`, `audit_logs`.

### تمرین
`exercise_catalog`, `exercise_media`, `workout_templates`, `workout_template_days`, `workout_exercises`, `workout_sets`, `workout_assignments`, `workout_assignment_versions`, `workout_sessions`, `workout_session_exercises`, `set_logs`, `personal_records`.

### تغذیه و سلامت غیرپزشکی
`nutrition_profiles`, `nutrition_targets`, `meal_plans`, `meal_plan_items`, `food_catalog`, `food_log_entries`, `body_measurements`, `progress_photos`, `wellness_checkins`.

### کسب‌وکار و عملیات
`plans`, `subscriptions`, `invoices`, `payment_transactions`, `payment_webhook_events`, `notifications`, `notification_preferences`, `tickets`, `ticket_messages`, `content_items`, `content_revisions`.

### AI و داده
`knowledge_documents`, `knowledge_chunks`, `embeddings`, `ai_conversations`, `ai_messages`, `ai_runs`, `ai_feedback`, `safety_events`, `outbox_events`, `analytics_events`.

### کلیدهای مهم و قیود
- همهٔ جداول: UUID/ULID، `created_at`, `updated_at`, و در داده‌های قابل حذف `deleted_at`.
- `users.email` و provider external id یکتا؛ `payment_webhook_events(provider,event_id)` یکتا؛ `set_logs(session_exercise_id,set_number)` یکتا.
- PII و دادهٔ حساس در ستون/باکت جدا با encryption؛ عکس‌ها فقط با `storage_object_id` ارجاع داده شوند.
- `tenant_id` از روز اول در طراحی در نظر گرفته شود اگر باشگاه/سازمان هدف آینده است؛ برای B2C ساده می‌تواند nullable باشد.

---

## 7) User flows و Journey

### User
1. نصب/ورود → پذیرش حریم خصوصی و سلب مسئولیت پزشکی.
2. onboarding کوتاه → هدف، تجربه، زمان، تجهیزات، محدودیت‌ها.
3. دریافت برنامهٔ مربی یا template/AI draft → مشاهده و تأیید.
4. صفحهٔ «امروز» → اجرای تمرین، ثبت هر ست/RPE، ثبت حس جلسه.
5. پایان هفته → یادآوری وزن/اندازه، نمودار و insight قابل فهم.
6. در صورت ابهام → AI Coach با citation یا تیکت/پیام به مربی.
7. تمدید اشتراک بدون قطع دسترسی ناخواسته و با اعلام قبلی.

### Coach
1. احراز هویت/تأیید ادمین → تکمیل تخصص و ظرفیت.
2. دعوت/پذیرش ورزشکار → مشاهدهٔ پروفایل مجاز و هدف.
3. ساخت از template یا AI draft → بررسی ایمنی، publish نسخهٔ برنامه.
4. inbox هشدار: عدم پایبندی، plateau، check-in جدید.
5. بازبینی هفتگی → note، تغییر نسخهٔ بعدی، پاسخ به کاربر.
6. گزارش ظرفیت، retention و وضعیت درآمد/اشتراک.

### Admin
1. ورود با MFA → داشبورد سلامت، فروش و صف‌های moderation.
2. تأیید مربی/مدیریت نقش با اصل چهارچشم برای عملیات حساس.
3. مدیریت کتابخانهٔ حرکات، محتوا و منابع دانش RAG با revision/publish.
4. رسیدگی تیکت، پرداخت ناموفق و safety incident.
5. گزارش KPI، export دارای مجوز، audit و تنظیمات feature flag.

---

## 8) AI: موارد استفاده و معماری ایمن

### موارد استفادهٔ مجاز
| قابلیت | ورودی | خروجی/کنترل |
|---|---|---|
| برنامهٔ تمرینی شخصی | هدف، تجربه، تجهیزات، زمان، محدودیت | draft ساختاریافتهٔ JSON؛ engine قواعد و coach/user تأیید می‌کنند |
| پیشنهاد تغذیه | هدف انرژی، ترجیح، آلرژی اعلام‌شده | ماکرو/وعدهٔ عمومی؛ هشدار برای شرایط پزشکی/اختلال خوردن |
| تحلیل پیشرفت | لاگ‌ها، وزن، adherence، wellness | insight احتمالی با confidence و درخواست check-in؛ نه ادعای قطعی |
| گفت‌وگوی Coach | پرسش کاربر + دانش تأییدشده | پاسخ با citation، escalation برای خطر |
| اصلاح برنامه | plateau/عدم پایبندی/feedback | تغییر پیشنهادی diff-based، هرگز overwrite خودکار |
| RAG داخلی | سند تأییدشده و metadata | بازیابی محدود به نسخه/زبان/سطح مخاطب |

### خط لولهٔ AI
```text
Request → identity/consent → input safety & risk classifier
 → context builder (profile minimization + recent logs)
 → RAG retrieval + citation filter
 → LLM (structured output/schema) → policy/rule validator
 → tool calls (read-only first) → response/draft + citations
 → feedback, audit, evaluation dataset
```

### Prompt engineering
- System prompt نسخه‌دار و غیرقابل تغییر توسط کاربر؛ نقش، ممنوعیت‌ها، زبان، عدم قطعیت و escalation را مشخص کند.
- Context فقط حداقل اطلاعات لازم باشد؛ injection موجود در اسناد RAG به‌عنوان دادهٔ غیرقابل‌اعتماد تلقی شود.
- خروجی با JSON Schema: `recommendation`, `rationale`, `risks`, `citations`, `follow_up_questions`, `requires_human_review`.
- نمونه: «برای هدف عضله‌سازی، بر اساس 3 جلسهٔ ثبت‌شده، یک پیش‌نویس 3 روزه بساز؛ آسیب زانو را رعایت کن؛ اگر اطلاعات کافی نیست فقط سؤال بپرس.»

### Tool calling
Tools با allow-list و سیاست نقش: `get_user_profile_minimum`, `get_recent_workouts`, `search_approved_knowledge`, `create_workout_draft`, `create_coach_review_task`. ابزار پرداخت، حذف داده، publish برنامه و دسترسی SQL مستقیم برای LLM ممنوع است. هر tool call validation، authorization، timeout و audit دارد.

### RAG / embedding / vector store
- اسناد منبع: راهنمای حرکات، سیاست محصول، محتوای nutrition تأییدشده، FAQ و دانش مربی تاییدشده.
- ingestion: پاک‌سازی → chunk 400–800 token با overlap → metadata (source, version, language, audience, reviewed_at) → embedding → pgvector.
- retrieval: hybrid (keyword + vector)، فیلتر metadata، rerank، حد آستانه و citation اجباری. اگر منبع کافی نبود، مدل باید «نمی‌دانم» بگوید.
- pgvector برای MVP؛ در حجم بسیار زیاد یا نیاز جست‌وجوی اختصاصی، Qdrant/Pinecone با همان interface.

### Memory و حریم خصوصی
- short-term: پیام‌های اخیر با سقف token.
- long-term: فقط خلاصهٔ تاییدشده/قابل مشاهده و preference صریح کاربر؛ TTL و امکان حذف.
- داده‌های حساس سلامت در prompt حداقل و با consent؛ training مدل با دادهٔ کاربر فقط opt-in صریح.

### Safety و moderation
- triage برای درد شدید، علائم قلبی/تنفسی، بارداری پرخطر، اختلال خوردن، خودآسیبی و درخواست دارو: توقف توصیه و ارجاع به پزشک/اورژانس محلی.
- فیلتر محتوای آسیب‌زا، توهین، تزریق prompt، PII leakage و خروجی خلاف policy.
- red-team سناریوهای فارسی/انگلیسی؛ evaluation آفلاین قبل از هر تغییر prompt/model.

---

## 9) UI/UX و Design System

### اصول
- **Mobile-first:** یک اقدام اصلی در صفحهٔ امروز؛ ثبت ست با حداقل لمس و قابلیت آفلاین.
- **شفاف و غیرقضاوتی:** به‌جای «شکست خوردی»، «۲ جلسه برای رسیدن به برنامهٔ این هفته باقی است».
- **دسترسی‌پذیر:** WCAG 2.2 AA، کنتراست، فونت قابل‌افزایش، target لمسی 44px، RTL واقعی و عدم اتکا به رنگ تنها.

### زبان بصری
- سبک: قدرتمند، آرام و داده‌محور؛ کارت‌های سبک، فضای سفید کافی، نمودار ساده، از neon/gradient افراطی اجتناب شود.
- رنگ پیشنهادی: Primary سبز/آبی انرژی‌بخش، Secondary بنفش ملایم، success سبز، warning کهربایی، danger قرمز؛ همه با token و حالت dark.
- تایپوگرافی فارسی: Vazirmatn یا Estedad؛ لاتین Inter. مقیاس 12/14/16/20/24/32.
- Tokenها: color, spacing (4px grid), typography, radius, elevation, motion, breakpoints؛ در Figma و کد یک منبع حقیقت.

### کامپوننت‌های اولویت‌دار
App shell، bottom navigation، workout timer، set logger، exercise card/video، progress chart، macro ring، calendar، coach client table، AI chat با citation، modal/confirm، form validation، toast و empty/error/offline states.

### تفاوت پلتفرم
- موبایل: Today، session، check-in، push؛ navigation پایین.
- وب/دسکتاپ: سازنده drag-and-drop برنامه، جدول ورزشکاران، نمودار عمیق، CMS و ادمین؛ sidebar و shortcut.

---

## 10) امنیت، حریم خصوصی و انطباق

1. **Authentication:** OIDC، MFA اجباری برای admin/coach، hash رمز با Argon2id، refresh-token rotation، revoke device/session، OTP rate-limited.
2. **Authorization:** RBAC + ownership/assignment (ABAC) در هر endpoint و query؛ deny-by-default؛ policy test.
3. **API:** TLS 1.2+، schema validation، CORS محدود، CSRF برای cookie، pagination limits، idempotency key برای mutation حساس، rate limit per IP/user/token.
4. **Data protection:** encryption at rest و in transit، KMS/secret manager، جداسازی PII، data retention/deletion/export، log redaction.
5. **File security:** direct upload با URL کوتاه‌عمر و content-type/size allow-list، اسکن malware، image re-encode، bucket private، دانلود URL امضاشده.
6. **Payment:** tokenization provider، عدم نگهداری PAN/CVV، signature verification، webhook replay protection، ledger تغییرناپذیر.
7. **AppSec:** SAST/DAST/dependency scanning، SBOM، patch SLA، pentest قبل از launch، threat modeling برای auth/payment/AI/file upload.
8. **AI security:** عدم ارسال secret/PII غیرضروری، tool sandbox، prompt injection protection، audit و human escalation.

---

## 11) Deployment، عملیات و مقیاس

### محیط‌ها و CI/CD
- محیط‌های `dev`, `staging`, `production` با حساب/secret مجزا.
- Pull request: lint, typecheck, unit, integration, migration check, SAST و build image.
- release: deploy canary/blue-green، migration backward-compatible، smoke test، امکان rollback.
- IaC با Terraform؛ image immutable در registry؛ secrets فقط در Secret Manager.

### Monitoring و logging
- SLI/SLO: API availability 99.9٪، p95 read < 400ms، p95 mutation < 700ms، queue lag، notification delivery، payment webhook success.
- trace ID از client تا worker؛ structured JSON logs؛ حذف token، email، key و داده سلامت از log.
- Sentry برای error، Prometheus/Grafana برای metric، Loki/Cloud logs برای log؛ alert با runbook و owner.

### backup و disaster recovery
- PostgreSQL: point-in-time recovery + snapshot روزانه؛ restore آزمایشی ماهانه.
- Object storage: versioning/lifecycle و replication در صورت نیاز.
- RPO اولیه: 15 دقیقه؛ RTO اولیه: 4 ساعت. runbook حادثه و تمرین recovery فصلی.

### scaling
- API stateless و horizontal autoscaling؛ Redis/DB managed و read replica وقتی لازم شد.
- workerها بر مبنای queue depth؛ CDN برای media؛ connection pooling.
- ابتدا DB را با index، query budget و archive بهینه کنید؛ partitioning رویداد/لاگ پیشرفت قبل از sharding.

---

## 12) نقشهٔ راه اجرایی و اولویت‌ها

### فاز 1 — تحلیل و طراحی (3 تا 5 هفته) — P0
- PRD، personas، KPI و scope MVP.
- research کاربر/مربی (حداقل 8 مصاحبه از هر گروه)، user journey، IA و wireframe.
- domain model، API contract، threat model، data classification و معماری تصمیم‌گیری (ADR).
- Design system foundations و prototype تست‌شده.
- CI/CD، محیط staging، observability skeleton و backlog برآوردشده.

**خروجی پذیرش:** PRD امضاشده، prototype با usability test، schema/API v1، release plan و معیارهای launch.

### فاز 2 — MVP (10 تا 14 هفته) — P0 سپس P1
- Sprint 1–2: auth، RBAC، profile/onboarding، catalog، app shell.
- Sprint 3–5: برنامه و اجرای تمرین، progress log/photo، dashboard پایه.
- Sprint 6–7: coach workspace، assignment/versioning، notification.
- Sprint 8: billing/payment webhook، entitlements، admin پایه و support.
- Sprint 9–10: AI RAG محدود/draft، safety، analytics، hardening و beta.

**معیار خروج:** user می‌تواند از onboarding تا چهار هفته تمرین را کامل کند؛ coach یک برنامه را نسخه‌بندی کند؛ پرداخت و دسترسی قابل اتکا؛ هیچ P0 security defect باز نباشد.

### فاز 3 — نسخهٔ حرفه‌ای (8 تا 12 هفته) — P1
- nutrition log و meal plan بهتر، template library، coach notes/inbox، گزارش‌های پیشرفته.
- پرداخت دوره‌ای/کد تخفیف، multi-language، A/B testing، data warehouse.
- AI insight با evaluation dashboard، پوشیدنی‌ها (پس از اعتبارسنجی نیاز).

### فاز 4 — کیفیت، امنیت و بهینه‌سازی (مداوم؛ milestone 4 هفته) — P0
- load/performance test، accessibility audit، pentest، DR restore drill.
- test automation E2E، chaos/retry tests برای payment/notification، cost/performance tuning.

### فاز 5 — انتشار و رشد (4 تا 8 هفته، سپس مداوم) — P0/P1
- closed beta (50–200 کاربر)، funnel/retention review، رفع friction.
- phased launch، support SLA، برنامه محتوا و referral پس از اثبات retention.
- برنامهٔ رشد فقط پس از رسیدن به activation و adherence هدف.

---

## 13) تیم، ترتیب اجرا و پیچیدگی

| نقش | مسئولیت | درگیری |
|---|---|---|
| Product Manager | PRD، KPI، backlog، discovery و release | تمام‌وقت |
| Tech Lead/Architect | ADR، مرز ماژول، کیفیت فنی، review | تمام‌وقت |
| Product Designer + UX Research | flow، prototype، DS، تست کاربر | تمام‌وقت فاز 1–2 |
| 2 Backend Engineers | domain/API، billing، queue، data | تمام‌وقت |
| 2 Frontend Engineers | Next.js/admin، React Native، DS | تمام‌وقت |
| AI Engineer | RAG، guardrail، eval، gateway | نیمه‌وقت MVP، تمام‌وقت فاز 3 |
| DevOps/SRE | IaC، CI/CD، observability، security baseline | نیمه‌وقت سپس on-call |
| QA Automation | test strategy، E2E، regression، release gate | تمام‌وقت از sprint 2 |
| Security Specialist | threat model، review، pentest coordination | پاره‌وقت/milestone |
| Fitness + Nutrition Experts | catalog، policy AI، content review | پاره‌وقت مستمر |

### ترتیب وابستگی
Discovery/design → identity + data foundation + DS → training/progress → coach workflow → billing/notification → AI محدود → beta/hardening. پرداخت و AI نباید مسیر اصلی ثبت تمرین را بلوکه کنند.

### برآورد پیچیدگی
- High: workout versioning/logging، RBAC ownership، payment webhooks، AI safety/RAG، offline sync.
- Medium: onboarding، dashboard، notifications، CMS/tickets.
- Low: marketing pages، export محدود، static content.

---

## 14) QA و تعریف Done

### هرم تست
- Unit: محاسبهٔ volume/adherence/macros، policy authorization، validators.
- Integration: DB migrations، API، outbox/queue، payment webhook idempotency.
- E2E: onboarding → assignment → log workout → progress → entitlement.
- Nonfunctional: load، accessibility، offline/reconnect، امنیت و restore.

هر داستان Done است اگر: acceptance criteria، طراحی، telemetry event، unit/integration لازم، i18n/RTL، error/empty/loading state، authorization، و مستند API تکمیل شده باشد.

---

## 15) ریسک‌ها و کاهش آن‌ها

| ریسک | اثر | کاهش |
|---|---|---|
| توصیهٔ ناایمن AI/سلامت | بسیار بالا | scope غیرپزشکی، guardrail، human review، escalation و expert review |
| scope creep | بالا | MVP سخت‌گیرانه، KPI gate، backlog P0/P1/P2 |
| حفظ کاربر پایین | بالا | user research، onboarding کوتاه، یادآوری هوشمند، cohort analytics |
| نشت عکس/داده حساس | بسیار بالا | private storage، signed URL، encryption، access audit و retention |
| خطای پرداخت | بالا | adapter، webhook idempotent، reconciliation و manual fallback |
| پیچیدگی multi-platform | متوسط | shared TS/domain contracts، PWA ابتدا، native فقط برای ارزش ثابت‌شده |
| هزینهٔ LLM | متوسط | RAG، cache، token budget، model routing و observability |
| کیفیت کاتالوگ تمرین/تغذیه | بالا | expert governance، versioning و review workflow |

---

## 16) چک‌لیست گام بعدی (دو هفتهٔ اول)

1. نام محصول، بازار/کشور، مدل درآمد، مخاطب اول و محدودیت‌های قانونی را نهایی کنید.
2. با 8 ورزشکار و 8 مربی مصاحبه کنید؛ مشکل، فرایند فعلی و willingness-to-pay را ثبت کنید.
3. PRD یک‌صفحه‌ای MVP و KPIهای activation/adherence را تأیید کنید.
4. در Figma، onboarding، Today، logger تمرین، progress و coach assignment را prototype کنید و 5 usability test انجام دهید.
5. repository monorepo (`apps/mobile`, `apps/web`, `apps/api`, `packages/ui`, `packages/contracts`) و CI پایه بسازید.
6. ADRهای Auth، payment region، data residency، AI provider و storage را ثبت کنید.
7. threat model و privacy notice را قبل از جمع‌آوری اولین دادهٔ واقعی تکمیل کنید.
8. یک vertical slice واقعی بسازید: signup → onboarding → برنامهٔ یک‌روزه → ثبت ست → dashboard؛ سپس با کاربران beta آزمایش کنید.

## خلاصهٔ تصمیم اجرایی

در نسخهٔ اول، یک محصول ساده اما کامل برای «دریافت برنامه، اجرای تمرین، ثبت پیشرفت و بازخورد مربی/AI ایمن» بسازید. Next.js/React Native/NestJS/PostgreSQL/Redis/S3، با monolith ماژولار و AI پشت guardrail، مناسب‌ترین نقطهٔ شروع قابل نگهداری است. ارزش اصلی باید با شاخص‌های activation، پایبندی هفتهٔ چهارم و بهره‌وری مربی اثبات شود؛ قابلیت‌های پرزرق‌وبرق مانند تشخیص ویدئو، شبکه اجتماعی و wearables تنها پس از آن وارد شوند.
