<img src="./media/image1.jpeg" style="width:6.5in;height:4.87847in" />
<div style="text-align: right">
# **<u>תוכן עניינים</u>**

**מבוא3**

**תיאור הבעיה3**

**תיאור הפתרון4**

**מבט על של התוכנה7**

**הדגמת ריצה8**

**גרפים ונתונים עבור ריצות שונות10**

**מסקנות וסיכום14**

**<span dir="rtl"><u>מבוא:</u></span>**

Movie recommender systems <span dir="rtl">הינה מערכת שממליצה למשתמש על
סרטים על פי העדפה אישית.</span> <span dir="rtl">  
</span>

<span dir="rtl">  
**<u>תיאור הבעיה:</u>**</span>

<span dir="rtl">בעידן של היום, בו קיימים שירותי סטרימינג וספריות וידאו
דיגיטליות עם כמויות אדירות של סרטים, נוצר צורך לבצע סינון כלשהו עבור
הצופה על מנת לספק לו את התכנים המתאימים ביותר.  
<u>  
**חלוקת הבעיה:**</u></span>

1.  <span dir="rtl"><u>**יצירת רשימת סרטים:**  
    </u>האפליקציה צריכה לספק סרטים עליהם נוכל לבצע את הבדיקה ובסוף להציע
    למשתמש את הסרטים המתאימים לו מרשימה זו.</span>

2.  **<span dir="rtl"><u>קריטריונים:</u></span>**

<span dir="rtl">על מנת לספק סרטים המתאימים להעדפה של המשתמש עלינו ליצור
רשימת קריטריונים אותם נוכל לדרוש לפיהם האפליקציה תקבל מידע לגבי העדפות
המשתמש.</span>

3.  **<span dir="rtl"><u>חישוב התאמה לכל סרט:</u></span>**

<span dir="rtl">לאחר שיצרנו רשימת סרטים עלינו לחשב התאמה של כל סרט
ברשימה זו לקריטריונים שהמשתמש סיפק.</span>

4.  **<u><span dir="rtl">חיפוש הסרטים המתאימים</span>:</u>**

<span dir="rtl">לאחר שנחשב לכל סרט את מידת ההתאמה שלו בהתאם לקריטריונים
של המשתמש נרצה להחזיר רשימה של הסרטים המתאימים ביותר.</span>

**<span dir="rtl"><u>תיאור הפתרון:</u></span>**

<span dir="rtl">על מנת להתמודד עם הבעיה יצרנו אפליקציה שמבקשת מהמשתמש
העדפה עבור מספר קריטריונים ומחזירה לו פלט של הסרטים המתאימים ביותר.
מימוש הפתרון נעשה באמצעות ספריית</span> Ec-Kity <span dir="rtl">שמספקת
לנו גישה נוחה לעבודה עם אלגוריתמים אבולוציוניים. התוכנית תקבל רשימת
סרטים קיימים והעדפות משתמש ולאחר ביצוע אלגוריתם אבולציוני מחזירה את
הסרטים המתאימים ביותר. במימוש שלנו החלטנו לבצע אלגוריתם אבולוציוני
באמצעות וקטורים עליו נפרט בהמשך.</span>

**<span dir="rtl"><u>חלוקת שלבי הפתרון:</u></span>**

1.  <span dir="rtl"><u>**יצירת רשימת סרטים:**  
    </u>התוכנית שולחת בקשות ל-</span>API <span dir="rtl">קיים שמבוסס על
    התוכן ב-</span>Netflix <span dir="rtl">ישראל שמתוכו אנו בונים</span>
    database <span dir="rtl">לוקאלי עדכני של סרטים.</span>

**<span dir="rtl">מגבלות:</span>**

<span dir="rtl">לא מצאנו</span> API <span dir="rtl">חינמי של סרטים,
ה-</span>API <span dir="rtl">איתו אנו עובדים מוגבל בכמות בקשות.</span>

<span dir="rtl">  
**פתרון למגבלות:**</span>

<span dir="rtl">בקשה חד פעמית של כמות מידע אפשרית מה-</span>API <span
dir="rtl">ויצירת</span> database <span dir="rtl">לוקאלי.</span>

2.  **<span dir="rtl"><u>קריטריונים:</u></span>**

<span dir="rtl">לאחר התבוננות בשדות החוזרים עבור כל סרט ב-</span>API
<span dir="rtl">איתו אנו עובדים בחרנו את השדות המתאימים ביותר לדירוג סרט
על ידי הצופה. השדות שנבחרו הינם: ז'אנר, שפת מקור, שנת יציאה מינמלית
ואורך סרט מקסימלי.  
נוסף על כך ישנה התחשבות בקריטיריון נוסף שאינו תלוי במשתמש וזהו קריטריון
דירוג הסרט ב-</span>IMDB<span dir="rtl">.</span>

<span dir="rtl">**חישוב ציון לכל סרט:**<u>  
</u>לאחר שהמשתמש סיפק את המידע הדרוש בהתאם לשדות המתאימים מתבצע חישוב
ציון ההתאמה עבור כל הסרטים, חישוב זה מבוצע פעם אחת שבסופו נקבל
בחזרה</span>

<span dir="rtl">וקטור -</span> movieScores<span dir="rtl">, בו כל אינדקס
מייצג את ציון הסרט המתאים לו ברשימת הסרטים.</span>

<span dir="rtl">**פירוט חישוב הציון לכל סרט:  
**בתחילת העבודה על הפרוייקט קבענו חלוקה שווה לכל אחד מהפרמטרים אך לאחר
קבלת תוצאות רבות שאינן רלוונטיות נתנו למשתמש שתי אפשרויות חדשות:  
1. לבצע את­­ התיעדוף לכל קריטריון בעצמו.</span>

<span dir="rtl">2. לעבוד עם חלוקה דיפולטיבית (עליה אנו ממליצים).</span>

<span dir="rtl">  
החישוב מתבצע באמצעות הפונקציה</span> grading_movies<span dir="rtl">,
שמקבלת כארגומנטים את תיעדוף הקריטריונים של המשתמש ,רשימת הסרטים ומספר
הז'אנרים שנבחרו על ידי המשתמש.  
הפונקציה מבצעת חישוב קבוע מראש על פי החלוקה לאחוזים שנקבעה על ידי המשתמש
תוך כדי התייחסות גם לדירוג הסרט ב-</span>IMDB<span dir="rtl">.  
סך כל העדפות המשתמש מקבל נקודה 1 ודירוג הסרט</span> IMDB <span
dir="rtl">מקבל נקודה 1, סה"כ הציון הגבוה ביותר שסרט יכול לקבל הוא 2
נקודות.</span>

3.  **<u><span dir="rtl">חיפוש הסרטים המתאימים</span>:</u>**

<span dir="rtl">לאחר שיצרנו את הווקטור</span> movieScores <span
dir="rtl">אנו מתחילים בשלב האלגוריתם האבולוציוני.  
האלגוריתם מייצר</span> initial-population <span dir="rtl">שמורכבת
מ-</span>individuals<span dir="rtl">, כאשר כל</span> individual <span
dir="rtl">מאותחל באופן אקראי.</span> Individual <span dir="rtl">הוא
וקטור של ביטים (</span>0 <span dir="rtl">עבור אי-המלצה ו-1 עבור המלצה)
שאורכו כמספר הסרטים הכולל וכל אינדקס בו מתאים לאינדקס של סרט
ב-</span>movieScore<span dir="rtl">.</span>

<span dir="rtl">לכל</span> individual <span dir="rtl">נרצה לבצע חישוב
של</span> fitness <span dir="rtl">שזהו למעשה חישוב התאמה מיטבית למערך
אשר מתבסס על ציוני ההתאמה ב-</span>movieScores<span dir="rtl">.</span>

<span dir="rtl">נשים לב כי מדובר בבעיית מקסימום עליה נפרט בהמשך.</span>

**<span dir="rtl">חישוב</span> fitness<span dir="rtl">:</span>**

<span dir="rtl">  
נשתמש במחלקה</span> movieEvaluator <span dir="rtl">הממששת את
הפונקציה</span> evaluate_individual()<span dir="rtl">.  
המחלקה מקבלת כארגומנטים את הווקטור</span> movieScores <span
dir="rtl">ואת השדה</span> lowerBoundGrade <span dir="rtl">המייצג את ציון
ההתאמה הנמוך ביותר שאנו מגדירים כמספק. בקוד שלנו בחרנו</span>
lowerBoundGrade = 1.5<span dir="rtl">, הסיבה לכך היא על מנת להבטיח כי גם
סרט שמדורג עם הציון הכי גבוה שניתן לבחור (100), יקבל תוצאה טובה שתאפשר
לו להכנס לרשימה אך ורק אם אחוז ההתאמה שלו לקריטריונים של המשתמש הוא
לפחות 50 אחוז.</span>

<span dir="rtl">הפונקציה</span> evaluate_individual() <span
dir="rtl">רצה באופן הבא:</span>

<span dir="rtl">  
לכל אינדקס</span> i <span dir="rtl">בווקטור</span> individual <span
dir="rtl">המייצג סרט:</span>

<span dir="rtl">אם הסרט ב-</span>movieScores\[i\] <span dir="rtl">גדול
שווה ל-</span>lowerBoundGrade <span dir="rtl">אז נכפול את הציון</span>

> <span dir="rtl">ב-</span>individual\[i\]<span dir="rtl">.  
> אחרת, נכפול את</span> individual\[i\] <span dir="rtl">בערך שלילי של
> תוצאת חיסור הציון מפרמטר הניקוד (נקודה אחת עבור דירוג הסרט ונקודה
> נוספת עבור הקריטריונים של המשתמש).  
> באופן זה כל הסרטים שלא עברו את סף ה-</span> lowerBoundGrade<span
> dir="rtl">יקבלו ציון שלילי אך סרטים שקרובים יותר לסף יקבלו ציון גבוה
> יותר (קרוב יותר ל-0) מאשר סרטים שרחוקים מהסף.</span>
>
> <span dir="rtl">נחבר את הערכים שהתקבלו מכל איטרציה והערך הסופי מייצג
> את ה-</span>fitness<span dir="rtl">. נרצה לקבל ציון הכי גבוה עבור
> ה-</span>fitness <span dir="rtl">לכן הגדרנו</span> higher is better =
> true<span dir="rtl">.</span>
>
> **genetic operators<span dir="rtl">:</span>**
>
> <span dir="rtl">  
> השתמשנו בשני סוגי ה-</span>genetic operators <span
> dir="rtl">הבסיסיים</span> CrossOver <span
> dir="rtl">ו-</span>Mutation<span dir="rtl">.בהרצות הראשונות עבדנו
> עם</span> data base <span dir="rtl">קטן יחסית (כ-30 סרטים) ועבור הכמות
> הזו השתמשנו ב:  
> </span>VectorKPointsCrossover <span
> dir="rtl">ו-</span>BitStringVectorNFlipMutation <span
> dir="rtl">הנתונים בחבילה</span> Ec-Kity<span dir="rtl">.  
> </span>
>
> <span dir="rtl">עבור מספר סרטים קטן קיבלנו תוצאות טובות בשימוש עם
> ה-</span> genetic operators<span dir="rtl">הללו.</span>
>
> <span dir="rtl">לאחר הגדלת ה-</span>data base <span dir="rtl">הגענו
> למספר של כ-560 סרטים ונתקלנו בבעיה להגיע לתוצאה מיטבית.</span>
>
> <span dir="rtl">לאחר מספר ניסויים שמנו לב כי הגדלת האוכלוסייה מסייעת
> להגיע לתוצאה טובה יותר, אך ככל שהגדלנו את האוכלוסייה נתקלנו בחישובים
> כבדים יותר שלקחו המון זמן.  
> על מנת להימנע מחישובים כבדים עקב גישת הגדלת האוכלוסייה החלטנו לנסות
> לבצע שינוי באופן הפעולה של ה-</span> genetic operators<span
> dir="rtl">בהם אנו משתמשים. תחילה ניסינו ליצור</span> Crossover <span
> dir="rtl">חדש:</span>

- <u>VectorKPointsCrossoverStrongestCross</u><span dir="rtl">:</span>

> <span dir="rtl">  
> ניסיון ראשון:</span>
>
> <span dir="rtl">בתהליך הזה אנו בוחרים נקודה רנדומלית בה נחלק כל אחד
> מההורים באופן דומה לחלוקה ב-</span> VectorKPointsCrossover <span
> dir="rtl">ונבדוק מיהו הווקטור הטוב ביותר הנוצר מבין השניים הבאים:  
> ילד שנוצר מהחלק הימני של הורה 1 והחלק השמאלי של הורה 2,</span>

<span dir="rtl">ילד שנוצר מהחלק הימני של הורה 2 והחלק השמאלי של הורה
1.</span>

<span dir="rtl">התהליך שיפר במקצת את התוצאות אך עדיין לא הגיע לתוצאה
מספקת.</span>

> <span dir="rtl">ניסיון שני:</span>
>
> <span dir="rtl">בתהליך הזה אנו בוחרים נקודה רנדומלית בה נחלק כל אחד
> מההורים בצורה דומה לחלוקה ב-</span> VectorKPointsCrossover<span
> dir="rtl">, בשונה מהניסיון הראשון הפעם נתבונן גם בהורים ונבדוק מיהו
> הוקטור הטוב ביותר הנוצר מבין הארבעה הבאים:  
> הורה 1,  
> הורה 2,  
> ילד שנוצר מהחלק הימני של הורה 1 והחלק השמאלי של הורה 2,</span>
>
> <span dir="rtl">ילד שנוצר מהחלק הימני של הורה 2 והחלק השמאלי של הורה
> 1.  
>   
> התהליך גם שיפר את התוצאות אך עדיין לא בצורה מספקת.</span>

<span dir="rtl">לאחר שיצירת</span> VectorKPointsCrossoverStrongestCross
<span dir="rtl">לא סיפק פתרון מיטבי לבעיה החלטנו לייצר גם</span>
Mutation operator <span dir="rtl">חדש –</span>
PrioritizedBitStringVectorNFlipMutation<span dir="rtl">.</span>

- <u>PrioritizedBitStringVectorNFlipMutation<span dir="rtl">:</span></u>

> <span dir="rtl">בתהליך זה נבצע</span> bit-mutation <span
> dir="rtl">בצורה הסתברותית בדומה לדרך בה פועל</span>
> BitStringVectorNFlipMutation <span dir="rtl">אך בשונה ממנו, לאחר
> הבחירה ההסתברותית אם נבחר לבצע</span> bit-flip <span dir="rtl">נפעיל
> שני אילוצים נוספים</span>:

1.  <span dir="rtl">אם</span> individual\[i\]=1 <span dir="rtl">וגם
    קיבלנו תוצאה שווה גדולה ל-</span> lowerBoundGrade <span dir="rtl">לא
    נבצע</span> bit-flip<span dir="rtl">.</span>

2.  <span dir="rtl">אם</span> individual\[i\]=0 <span dir="rtl">וגם
    קיבלנו תוצאה מתחת ל-</span>lowerBoundGrade <span dir="rtl">לא
    נבצע</span> bit-flip<span dir="rtl">.</span>

> <span dir="rtl">לאחר הוספת</span>
> PrioritizedBitStringVectorNFlipMutation <span dir="rtl">התוצאות
> שקיבלנו השתפרו לרמת פלט מספקת גם במימוש עם</span>
> VectorKPointsCrossoverStrongestCross <span dir="rtl">אותו יצרנו וגם
> במימוש</span> VectorKPointsCrossover <span dir="rtl">שהיה קיים
> בחבילת</span> Ec-Kity<span dir="rtl">.</span>
>
> **Selection<span dir="rtl">:</span>**

<span dir="rtl">בחרנו להשתמש ב-</span>tournament selection <span
dir="rtl">בגודל 2 ו-</span>higher is better = true<span dir="rtl">.  
</span>

**<span dir="rtl"><u>מבט על של התוכנה:</u></span>**

<span dir="rtl">התוכנה מבצעת אתחול של ה-</span>data base <span
dir="rtl">(במידה ולא קיים) באמצעות הפונקציה</span> load_movies<span
dir="rtl">.</span>

<span dir="rtl">התוכנה מקבלת מהמשתמש מידע לגבי דירוג הקריטריונים.</span>

<span dir="rtl">התוכנה מבצעת חישוב של דירוג הסרטים על סמך דירוג המשתמש
באמצעות הפונקציה</span> grading_movies<span dir="rtl">.</span>

<span dir="rtl">התוכנה מבצעת אתחול של האלגוריתם.</span>

<span dir="rtl">התוכנה מבצעת</span> algo.evolve() <span dir="rtl">ותתחיל
את ריצת האלגוריתם האבולוציוני.</span>

<span dir="rtl">התוכנה תריץ את</span> algo.execute() <span
dir="rtl">ותשמור את וקטור הפלט הטוב ביותר ב-</span>result<span
dir="rtl">.</span>

<span dir="rtl">במידה והאלגוריתם לא מצא סרטים מתאימים נאפשר למשתמש
להכניס קריטריונים חדשים.</span>

<span dir="rtl">במידה והאלגוריתם מצא לפחות סרט אחד נחזיר למשתמש רשימת
סרטים אפשריים</span> <span dir="rtl">אחרת נאפשר למתשמש להזין נתונים
חדשים.</span>

**<span dir="rtl"><u>הדגמת ריצה:</u></span>**

<span dir="rtl">המשתמש מקבל אפשרות לבחור האם להזין בעצמו את המשקל לכל
קריטריון או להחליט על המשקל בעצמו.</span>

<img src="./media/image2.png" style="width:6.5in;height:0.40486in" />

<span dir="rtl">נבצע ריצה עם ההמלצה שלנו:</span>

<img src="./media/image3.png" style="width:5.22464in;height:2.3019in" />

<span dir="rtl">המשתמש יבחר ז'אנר רצוי (אחד או יותר) ולאחר כל בחירה של
ז'אנר ילחץ על</span> enter<span dir="rtl">. לאחר שסיים לבחור את כל
הז'אנרים המשתמש יזין למסך את המילה</span> ‘finish’ <span dir="rtl">ולאחר
מכן ילחץ על</span> enter<span dir="rtl">.</span>

<img src="./media/image4.png"
style="width:5.02153in;height:0.43756in" />

<span dir="rtl">המתמש יבחר שפת מקור רצויה (אחת או יותר) באופן זהה לבחירת
הז'אנר.</span>

<img src="./media/image5.png" style="width:6.5in;height:0.80208in" />

<span dir="rtl">כעת המשתמש יבחר שנת יציאה מינימלית ואורך סרט
מקסימלי.</span>

<img src="./media/image6.png"
style="width:6.12586in;height:0.40631in" />

<span dir="rtl">האלגוריתם יעצור במידה והגיע להתאמה לפי
ה-</span>threshold <span dir="rtl"> (בקוד שלנו בחרנו 80 אחוז התאמה,
כלומר</span> threshold = 0.2 \* max_fitness<span dir="rtl">).</span>

<img src="./media/image7.png" style="width:2.0107in;height:1.26059in" />

<span dir="rtl">בסיום ריצת האלגוריתם האבולוציוני התוכנית תדפיס רשימה של
כל הסרטים המומלצים בהתאם לקריטריונים ודרישת המשתמש (במידה ולא נמצאו כאלה
התוכנית תציע למשתמש להתחיל את התהליך מחדש).</span>

<img src="./media/image8.png"
style="width:2.58369in;height:2.55244in" />

**<span dir="rtl"><u>גרפים ונתונים עבור ריצות שונות:</u></span>**

<span dir="rtl">**בכל דוגמאות ההרצה השתמשנו בנתונים זהים:**  
</span>population_size=300 <span dir="rtl">(שונה רק בריצה מספר 3)  
</span>MAX_GENERATION = 300

Genres: 10749, 35  
Original language = en  
Min year = 2000  
Max length = 130

<span dir="rtl">\*תזכורת – האלגוריתם יעצור לפני הגעה
ל-</span>MAX_GENERATION <span dir="rtl">אם מדד ה-</span>fitness <span
dir="rtl">גדול או שווה ל-80% מ-</span>max fitness<span
dir="rtl">.</span>

<span dir="rtl">**ריצה 1** –</span> data base <span dir="rtl">קטן של
סרטים עם</span> VectorKPointsCrossover <span
dir="rtl">ו-</span>BitStringVectorNFlipMutation<span dir="rtl">:</span>

Max fitness = 4.54  
matched movies = 3  
Best fitness = 3.72  
total movies in DB: 88  
recommended movies in DB: 4

<img src="./media/image9.png"
style="width:4.73393in;height:3.55045in" />

<span dir="rtl">**ריצה 2** –</span> data base <span dir="rtl">גדול של
סרטים עם</span> VectorKPointsCrossover <span
dir="rtl">ו-</span>BitStringVectorNFlipMutation<span dir="rtl">:</span>

Max Fitness = 31.11  
matched movies = 20  
Best Fitness = -27.540000000000003  
total movies in DB: 568  
recommended movies in DB: 86

<img src="./media/image10.png"
style="width:4.26387in;height:3.1979in" />

<img src="./media/image11.png"
style="width:4.43125in;height:3.32361in" /><span dir="rtl">**ריצה 3**
–</span> data base <span dir="rtl">גדול של סרטים עם</span>
VectorKPointsCrossover <span
dir="rtl">ו-</span>BitStringVectorNFlipMutation <span dir="rtl">עם הגדלה
של ה-</span>initial population<span dir="rtl">:</span>

<span dir="rtl"><u>שינוי אוכלוסייה מ-300 ל-5,000:</u></span>

Max fitness = 31.11  
matched movies = 20  
Best fitness = 19.28  
total movies in DB: 568  
recommended movies in DB: 33

<img src="./media/image12.png"
style="width:4.14394in;height:3.10795in" /><span dir="rtl"><u>שינוי
אוכלוסייה ל-10,000:</u></span>

Max fitness = 31.11  
matched movies = 20  
Best fitness = 25.28  
total movies in DB: 568  
recommended movies in DB: 27

**<span dir="rtl">ריצה</span> 4** <span dir="rtl">–</span> data base
<span dir="rtl">גדול של סרטים עם</span>
VectorKPointsCrossoverStrongestCross <span dir="rtl">
ו-</span>BitStringVectorNFlipMutation<span dir="rtl">:</span>

Max fitness = 31.11  
matched movies = 20  
Best fitness = -30.239999999999995  
total movies in DB: 568  
recommended movies in DB: 90

<img src="./media/image13.png"
style="width:4.22601in;height:3.16951in" />

**<span dir="rtl">ריצה</span> 5** <span dir="rtl">–</span> data base
<span dir="rtl">גדול של סרטים עם</span> VectorKPointsCrossover <span
dir="rtl"> ו-</span> PrioritizedBitStringVectorNFlipMutation<span
dir="rtl">:</span>

<img src="./media/image14.png" style="width:4.1in;height:3.075in" />Max
fitness = 31.11  
matched movies = 20  
Best fitness = 25.439999999999998  
total movies in DB: 568  
recommended movies in DB: 21

**<span dir="rtl">ריצה</span> 6** <span dir="rtl">–</span> data base
<span dir="rtl">גדול של סרטים עם</span>
VectorKPointsCrossoverStrongestCross <span dir="rtl"> ו-</span>
PrioritizedBitStringVectorNFlipMutation<span dir="rtl">:</span>

<img src="./media/image15.png"
style="width:3.93277in;height:2.94958in" />Max fitness = 31.11  
matched movies = 20  
Best fitness = 24.830000000000002  
total movies in DB: 568  
recommended movies in DB: 16

**<span dir="rtl"><u>מסקנות וסיכום:</u></span>**

<span dir="rtl">**נסכם את השינויים מריצה לריצה:**  
ריצה 1: קיבלנו תוצאה רצויה (מעל 80% אחוז התאמה) לאחר 40 דורות.  
ריצה 2: קיבלנו תוצאה לא רצויה, וכפי שניתן לראות קצב העלייה הופך לאיטי
יותר לאחר מספר דורות.  
ריצה 3: גם לאחר העלת האוכלוסייה לגודל של 5,000 עדיין לא הגענו לתוצאה
רצויה לאחר 300 דורות, עם זאת בריצה של אוכלוסייה בגודל של 10,000 הצלחנו
להגיע לתוצאה רצויה לאחר כ-200 דורות. ניתן לראות כי הגדלת האוכלוסייה
משפרת את התוצאה ואף עבור אוכלוסייה גדולה מספיק התוצאה הרצויה מתקבלת גם
לאחר פחות מ-300 דורות.  
ריצה 4: קיבלנו תוצאה לא רצויה, בדומה לריצה מספר 2, קצב העלייה הופך איטי
יותר לאחר מספר דורות.  
ריצות 5 ו-6: בשתי הריצות הללו קיבלנו תוצאה רצויה, ריצה 5 הצליחה לעצור
לאחר 100 דורות וריצה 6 לא עצרה לאחר 100 דורות אך ניתן להבחין לפי הגרף כי
החל מדור 150 לא היה שינוי בערך ה-</span>fitness <span dir="rtl">והתוצאה
מאוד קרובה ל-80% התאמה.  
כמו כן ניתן להבחין כי בריצה 6 קצב העלייה בין הדורות 0 ל-100 מהיר יותר
מקצב העלייה בריצה 5, כלומר שתי הריצות מגיעות לתוצאה הרצויה, אך ריצה 6
מגיעה לתוצאה זו בקצב מהיר יותר בעקבות השימוש ב-</span>
VectorKPointsCrossoverStrongestCross <span dir="rtl">שמתעדף את וקטור
הקרוס-אובר הטוב ביותר.</span>

<span dir="rtl">כפי שניתן לראות מהריצות השונות, עבור קלט קטן התוכנית
מצליחה להגיע לתוצאות טובות בשימוש עם</span> VectorKPointsCrossover <span
dir="rtl">ו-</span>BitStringVectorNFlipMutation<span dir="rtl">. אך כאשר
גודל הקלט עולה יש צורך להגדיל את גודל האוכלוסייה על מנת לשפר את התוצאות
של התהליך האבולוציוני. (ניתן גם לבצע שינוי בכמות הדורות על מנת לאפשר
איטרציות נוספות בניסיון לשפר את איכות הפלט)</span>

<span dir="rtl">עם זאת הגדלת אוכלוסייה היא פתרון בעייתי, שכן ככל שכמות
הסרטים תגדל כך נצטרך גם להגדיל את כמות האוכלוסייה בהתאם. פתרון זה אינו
יעיל ודורש חישובים כבדים ומחשבים חזקים יותר.</span>

<span dir="rtl">לסיכום לאחר הרצת כל ששת סוגי הריצה השונים מספר רב של
פעמים, ניתן להסיק כי הפתרון היעיל ביותר הוא שימוש ב-</span>
PrioritizedBitStringVectorNFlipMutation <span dir="rtl">שמבצע מוטציות רק
כאשר המוטציה משפרת את ה-</span>fitness <span dir="rtl">של הווקטור. גישה
זו נותנת תוצאות זהות גם עבור</span> VectorKPointsCrossover <span
dir="rtl">וגם עבור</span> VectorKPointsCrossoverStrongestCross <span
dir="rtl">גם כאשר גודל האוכלוסייה נשאר נמוך (300).</span>
</div>
