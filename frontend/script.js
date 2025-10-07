document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = 'http://127.0.0.1:8000';

    // Form and result elements
    const roiForm = document.getElementById('roi-form');
    const resultsContainer = document.getElementById('results-container');
    const actionsContainer = document.getElementById('actions-container');
    const notificationToast = new bootstrap.Toast(document.getElementById('notification-toast'));

    // Result display elements
    const monthlySavingsEl = document.getElementById('monthly_savings');
    const paybackMonthsEl = document.getElementById('payback_months');
    const roiPercentageEl = document.getElementById('roi_percentage');
    const netSavingsEl = document.getElementById('net_savings');

    // Buttons
    const saveScenarioBtn = document.getElementById('save-scenario-btn');
    const generateReportBtn = document.getElementById('generate-report-btn');
    const viewScenariosBtn = document.getElementById('view-scenarios-btn');
    const scenariosList = document.getElementById('scenarios-list');

    let currentSimulationData = null;
    let currentSimulationResults = null;
    let lastSavedScenarioId = null;

    // --- Event Listeners ---

    // Handle form submission to run simulation
    roiForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = getFormData();
        currentSimulationData = formData;

        try {
            const response = await fetch(`${API_BASE_URL}/simulate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail[0]?.msg || 'Simulation failed');
            }

            const results = await response.json();
            currentSimulationResults = results;
            displayResults(results);
            actionsContainer.classList.remove('d-none');
            showNotification('Simulation successful!', 'success');

        } catch (error) {
            console.error('Simulation Error:', error);
            showNotification(`Error: ${error.message}`, 'danger');
        }
    });

    // Handle "Save Scenario" button click
    saveScenarioBtn.addEventListener('click', async () => {
        if (!currentSimulationData) {
            showNotification('Please run a simulation first.', 'warning');
            return;
        }

        const scenarioData = {
            scenario_name: document.getElementById('scenario_name').value,
            ...currentSimulationData,
        };

        try {
            const response = await fetch(`${API_BASE_URL}/scenarios`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(scenarioData),
            });

            if (!response.ok) throw new Error('Failed to save scenario.');

            const savedScenario = await response.json();
            lastSavedScenarioId = savedScenario.id;
            showNotification(`Scenario "${savedScenario.scenario_name}" saved successfully!`, 'success');
            // Optionally, refresh the list of scenarios if it's visible
            if (!scenariosList.innerHTML.trim() == '') {
                loadScenarios();
            }
        } catch (error) {
            console.error('Save Scenario Error:', error);
            showNotification(`Error: ${error.message}`, 'danger');
        }
    });

    // Handle "Generate Report" button click
    generateReportBtn.addEventListener('click', async () => {
        if (!lastSavedScenarioId) {
            showNotification('Please save the current scenario before generating a report.', 'warning');
            return;
        }

        const email = prompt('Please enter your email to generate the report:');
        if (!email || !validateEmail(email)) {
            showNotification('A valid email is required to generate a report.', 'warning');
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/report/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ scenario_id: lastSavedScenarioId, email }),
            });

            if (!response.ok) throw new Error('Failed to generate report.');

            const result = await response.json();
            showNotification(`Report generated successfully! Saved at: ${result.file_path}`, 'success');

        } catch (error) {
            console.error('Generate Report Error:', error);
            showNotification(`Error: ${error.message}`, 'danger');
        }
    });

    // Handle "View Saved Scenarios" button click
    viewScenariosBtn.addEventListener('click', loadScenarios);

    // --- Helper Functions ---

    // Get all values from the form
    function getFormData() {
        const ids = [
            'monthly_invoice_volume', 'num_ap_staff', 'avg_hours_per_invoice',
            'hourly_wage', 'error_rate_manual', 'error_cost',
            'time_horizon_months', 'one_time_implementation_cost'
        ];
        const data = {};
        ids.forEach(id => {
            const element = document.getElementById(id);
            data[id] = element.type === 'number' ? parseFloat(element.value) : element.value;
        });
        return data;
    }

    // Display simulation results on the page
    function displayResults(results) {
        monthlySavingsEl.textContent = `$${results.monthly_savings.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        paybackMonthsEl.textContent = results.payback_months !== null ? `${results.payback_months.toFixed(2)} months` : 'N/A';
        roiPercentageEl.textContent = results.roi_percentage !== null ? `${results.roi_percentage.toFixed(2)}%` : 'N/A';
        netSavingsEl.textContent = `$${results.net_savings.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }

    // Load and display all saved scenarios
    async function loadScenarios() {
        try {
            const response = await fetch(`${API_BASE_URL}/scenarios`);
            if (!response.ok) throw new Error('Failed to fetch scenarios.');

            const scenarios = await response.json();
            scenariosList.innerHTML = ''; // Clear current list

            if (scenarios.length === 0) {
                scenariosList.innerHTML = '<p class="text-muted">No scenarios saved yet.</p>';
                return;
            }

            scenarios.forEach(scenario => {
                const item = document.createElement('a');
                item.href = '#';
                item.className = 'list-group-item list-group-item-action';
                item.innerHTML = `
                    <div class="d-flex w-100 justify-content-between">
                        <h5 class="mb-1">${scenario.scenario_name}</h5>
                        <small>ROI: ${scenario.roi_percentage !== null ? scenario.roi_percentage.toFixed(2) + '%' : 'N/A'}</small>
                    </div>
                    <p class="mb-1">Monthly Savings: $${scenario.monthly_savings.toLocaleString()}</p>
                `;
                item.addEventListener('click', (e) => {
                    e.preventDefault();
                    loadScenarioToForm(scenario);
                });
                scenariosList.appendChild(item);
            });
        } catch (error) {
            console.error('Load Scenarios Error:', error);
            showNotification(`Error: ${error.message}`, 'danger');
        }
    }

    // Populate the form with data from a saved scenario
    function loadScenarioToForm(scenario) {
        // Populate form fields
        for (const key in scenario) {
            const element = document.getElementById(key);
            if (element) {
                element.value = scenario[key];
            }
        }
        // Display results
        displayResults(scenario);
        // Update state
        currentSimulationData = getFormData();
        currentSimulationResults = scenario;
        lastSavedScenarioId = scenario.id;
        actionsContainer.classList.remove('d-none');
        showNotification(`Loaded scenario: "${scenario.scenario_name}"`, 'info');
        window.scrollTo(0, 0); // Scroll to top
    }

    // Show a toast notification
    function showNotification(message, type = 'info') {
        const toastBody = document.querySelector('#notification-toast .toast-body');
        const toastHeader = document.querySelector('#notification-toast .toast-header');

        toastBody.textContent = message;
        // Reset classes
        toastHeader.classList.remove('bg-success', 'bg-danger', 'bg-warning', 'bg-info', 'text-white');

        switch (type) {
            case 'success':
                toastHeader.classList.add('bg-success', 'text-white');
                break;
            case 'danger':
                toastHeader.classList.add('bg-danger', 'text-white');
                break;
            case 'warning':
                toastHeader.classList.add('bg-warning', 'text-white');
                break;
            default:
                toastHeader.classList.add('bg-info', 'text-white');
        }

        notificationToast.show();
    }

    // Simple email validation
    function validateEmail(email) {
        const re = /^(([^<>()[\]\.,;:\s@"]+(\.[^<>()[\]\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }
});
