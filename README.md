# Complyance_Assignment
Created for 3rd round process of complyance


# Invoicing ROI Simulator

A lightweight ROI calculator that helps users visualize the cost savings and payback period when switching from manual to automated invoicing. This project was built as a rapid prototype to demonstrate the value of automation.

 <!-- Replace with a real screenshot URL -->

##  Purpose

The goal of this application is to provide a simple, interactive tool for potential customers. By entering a few key business metrics, users can instantly see the financial benefits of adopting an automated invoicing solution. The calculator is intentionally designed with a "bias factor" to ensure the results always highlight a positive return on investment.

##  Features

-   **Instant Simulation:** An interactive form provides real-time calculations for monthly savings, total ROI, and payback period.
-   **Scenario Management:** Users can name and save their simulations for future reference. Saved scenarios can be loaded or deleted.
-   **Gated Report Generation:** Users can download a summary of their simulation as a PDF report after providing an email address for lead capture.
-   **RESTful API:** A clean backend API handles all calculations and data persistence.

##  Tech Stack

-   **Backend:** Node.js, Express.js
-   **Database:** SQLite
-   **Frontend:** HTML, CSS, Vanilla JavaScript
-   **PDF Generation:** `html-pdf`

##  Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Node.js (which includes npm) installed on your system.

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/aravindh49/Complyance_Assignment.git
    cd Complyance_Assignment
    ```

2.  **Install backend dependencies:**
    Navigate to the backend directory and install the required npm packages.
    ```sh
    cd backend
    npm install
    ```

### Running the Application

1.  **Start the backend server:**
    From the `backend` directory, run the following command. The server will start on `http://localhost:3000`.
    ```sh
    node server.js
    ```

2.  **Launch the frontend:**
    Open the `frontend/index.html` file directly in your web browser. The application is now ready to use!

## How to Test

1.  **Test Quick Simulation:**
    -   Enter values into the input fields (e.g., 2000 invoices, 3 staff, $30 wage).
    -   Verify that the "Live Results" section updates instantly.

2.  **Test Scenario Management:**
    -   After running a simulation, enter a name in the "Scenario Name" field and click "Save Scenario."
    -   Verify that the scenario appears in the "Saved Scenarios" list.
    -   Click "Load" to populate the form with its data.
    -   Click "Delete" to remove a scenario.

3.  **Test Report Generation:**
    -   Click the "Download Report" button.
    -   Enter an email in the modal that appears and click "Generate."
    -   A PDF file should be downloaded by your browser.

##  API Endpoints

| Method | Endpoint             | Description                                          |
| :----- | :------------------- | :--------------------------------------------------- |
| `POST` | `/simulate`          | Runs a simulation and returns JSON results.          |
| `POST` | `/scenarios`         | Saves a named scenario with its inputs.              |
| `GET`  | `/scenarios`         | Retrieves a list of all saved scenarios.             |
| `GET`  | `/scenarios/:id`     | Retrieves the details of a single scenario by its ID.|
| `DELETE`| `/scenarios/:id`    | Deletes a scenario by its ID.                        |
| `POST` | `/report/generate`   | Generates and returns a PDF report (requires email). |
