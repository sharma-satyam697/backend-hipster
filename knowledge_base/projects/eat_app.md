## EAT: Personalized AI-Powered Food, Wine & Cocktail Assistant

### 🥗 Overview
EAT is a personalized intelligent assistant designed to help users plan meals, discover recipes, and find the perfect wine or cocktail pairing — all powered by AI. The platform curates suggestions based on user preferences such as high-protein diets, calorie goals, or fiber-rich meals. Whether you're planning a fancy dinner or a quick brunch, EAT ensures you never miss a meal.

---

### 🗃️ Backend Dataset
The application is backed by a large and diverse database:
- **25,000+ wines** from around the world
- **13,000+ recipes** sourced from popular platforms like *AllRecipes* and *NYT Cooking*
- **6,000+ cocktails**, complete with names, ingredients, and tags

These collections offer a wide variety of options tailored to dietary goals, taste profiles, and meal times.

---

### 🔍 Key Features
- 🔍 **Recipe Recognition**: Upload a meal photo and get the most relevant recipe using GPT-4.1 Nano for accurate text-based identification.
- 🥂 **Wine & Cocktail Matching**: Snap a photo of a wine label or cocktail, and our **YOLO-based one-shot vision model** will find the closest match.
- 📦 **Smart Retrieval**: Uses **Qdrant vector database** to retrieve best-matched items based on:
  - Ingredients
  - Nutritional content
  - Regional origin
- 🍽️ **Meal Planning**: Schedule breakfast, lunch, dinner, or brunch. Get reminders so you never skip a meal.
- 🔔 **Notifications**: Automated **cron job system** sends push notifications via **Firebase** to remind users about scheduled meals.
- 🧠 **Preference-Aware Recommendations**: Suggests meals based on dietary goals (e.g., high protein, low carb, fiber-rich).

---

### 🧪 Tech Stack & Tools
- **MongoDB**: Stores flexible, unstructured data like user preferences, recipe metadata, and scan results
- **Qdrant**: Handles semantic search via vector similarity (e.g., for nutritional matching or ingredient overlap)
- **YOLO (Vision Model)**: Enables image-based search for wine and cocktail recognition
- **GPT-4.1 Nano API**: Extracts recipe names accurately from scanned meal text
- **Web-Scraper (Chrome Extension)**: Used for scraping structured recipe content from sites like AllRecipes and NYT Cooking
- **Firebase + Cron Jobs**: For push notifications and meal scheduling reminders

---

### 📦 Summary
EAT is more than just a recipe app — it's a smart assistant for your dining experience. From AI-powered image recognition to tailored nutritional suggestions, EAT brings intelligent automation to food and beverage planning. Whether you're a fitness enthusiast, a food lover, or just someone who forgets their lunch plan — EAT has your back.
