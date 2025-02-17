## ChatAppoint

ChatAppoint is an intelligent appointment scheduling application that allows users to book appointments through a simple chat interface. The chatbot guides users through the process by asking relevant questions such as vaccination type, date, and location, then suggests nearby pharmacies for the appointment.

### 🚀 Features

- 🗨️ **Chat-Based Interface**: Book appointments seamlessly with a conversational chatbot.
- 📍 **Location-Based Suggestions**: Recommends nearby pharmacies based on the user's location.
- 📅 **Flexible Scheduling**: Easily choose the date and time that fits your schedule.
- 💉 **Healthcare-Focused**: Supports booking for various vaccination types.
- 🔒 **Secure and Reliable**: Ensures data privacy and reliability throughout the process.

### 🛠️ Tech Stack

- **Frontend**: React/Next.js
- **Backend**: FastAPI
- **Chatbot**: OpenAI API
- **Database**: PostgreSQL
- **Maps & Location**: Google Maps API

### ⚙️ Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/ChatAppoint.git
   cd ChatAppoint
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Configure environment variables:

   - Create a `.env` file and add the following:

   ```bash
   PORT=5000
   DATABASE_URL=your_database_url
   OPENAI_API_KEY=your_chat_api_key
   ```

4. Start the application:

   ```bash
   npm run dev
   ```

### 🚶‍♂️ Usage

1. Open the application in your browser.
2. Start a chat with the ChatAppoint assistant.
3. Answer the assistant's questions regarding:
   - Vaccination type (e.g., flu, COVID-19, etc.)
   - Preferred appointment date and time
   - Your location
4. Select from the suggested pharmacies.
5. Confirm the appointment.

### 📖 Example Interaction

- User: "I need a COVID-19 vaccine."
- ChatAppoint: "Sure! What date and time would you prefer?"
- User: "Next Monday at 10 AM."
- ChatAppoint: "Got it. What's your location?"
- User: "Downtown Sydney."
- ChatAppoint: "Here are some nearby pharmacies: [Pharmacy A, Pharmacy B, Pharmacy C]."
- User: "Let's go with Pharmacy A."
- ChatAppoint: "Appointment confirmed for Monday at 10 AM at Pharmacy A."

### 🧩 Future Improvements

- Integration with more healthcare providers.
- Support for additional appointment types beyond vaccinations.
- Multi-language chatbot functionality.
- Mobile app support.

### 🛟 Support

For any questions or support, please contact [iamkarin.tech@gmail.com](mailto:iamkarin.tech@gmail.com).

---

Happy chatting with **ChatAppoint**! 🤖💉📅

