document.addEventListener('DOMContentLoaded', () => {
    // Check auth
    if (!localStorage.getItem('token')) {
        window.location.href = 'index.html';
        return;
    }

    // Logout
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('token');
            window.location.href = 'index.html';
        });
    }

    // Load Dashboard Stats
    const totalContracts = document.getElementById('total-contracts');
    const pendingReviews = document.getElementById('pending-reviews');
    const highRiskContracts = document.getElementById('high-risk-contracts');
    const upcomingDeadlines = document.getElementById('upcoming-deadlines');
    const contractsTableBody = document.getElementById('contracts-table-body');

    if (totalContracts && pendingReviews) {
        async function loadDashboardData() {
            try {
                const contracts = await api.get('/contracts');
                
                let pendingCount = 0;
                let highRiskCount = 0;
                let lowRiskCount = 0;
                let mediumRiskCount = 0;
                
                contracts.forEach(c => {
                    if (c.status === 'Pending Review' || c.status === 'Uploaded') pendingCount++;
                    // Assuming risk score or level is returned. Adapt if exact field differs.
                    const riskLevel = c.risk_level || 'Low';
                    if (riskLevel === 'High') highRiskCount++;
                    else if (riskLevel === 'Medium') mediumRiskCount++;
                    else lowRiskCount++;
                });

                totalContracts.textContent = contracts.length;
                pendingReviews.textContent = pendingCount;
                if (highRiskContracts) highRiskContracts.textContent = highRiskCount;
                if (upcomingDeadlines) upcomingDeadlines.textContent = '0'; // Real deadlines can be fetched later

                if (contractsTableBody) {
                    contractsTableBody.innerHTML = contracts.slice(0, 5).map(c => {
                        const risk = c.risk_level || 'Unknown';
                        let riskColor = 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300';
                        if (risk === 'Low') riskColor = 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400';
                        if (risk === 'Medium') riskColor = 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400';
                        if (risk === 'High') riskColor = 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400';

                        let statusColor = 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300';
                        if (c.status === 'Analyzed') statusColor = 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400';
                        
                        return `
                        <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="flex items-center">
                                    <i data-lucide="file-text" class="h-4 w-4 text-slate-400 mr-2"></i>
                                    <div>
                                        <div class="text-sm font-medium text-slate-900 dark:text-white">${c.filename || c.name || 'Document'}</div>
                                        <div class="text-xs text-slate-500">${c.contract_type || 'Unknown Type'}</div>
                                    </div>
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm text-slate-900 dark:text-slate-300">${c.party_name || c.counterparty || 'N/A'}</div>
                                <div class="text-xs text-slate-500">${new Date(c.upload_date || Date.now()).toLocaleDateString()}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${riskColor}">
                                    ${risk} Risk
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${statusColor}">
                                    ${c.status || 'Uploaded'}
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                <a href="analysis.html?id=${c.id}" class="text-brand-600 hover:text-brand-900 dark:text-brand-400 dark:hover:text-brand-300 mr-3">View</a>
                            </td>
                        </tr>
                        `;
                    }).join('');
                    
                    if (typeof lucide !== 'undefined') lucide.createIcons();
                }

                // Update Chart if it exists and we have data
                const riskChartCtx = document.getElementById('riskChart');
                if (riskChartCtx && window.myRiskChart) {
                    window.myRiskChart.data.datasets[0].data = [lowRiskCount, mediumRiskCount, highRiskCount, 0];
                    window.myRiskChart.update();
                }

            } catch (err) {
                console.error("Failed to load dashboard data", err);
            }
        }
        
        loadDashboardData();
    }

    // Chart.js implementation for Risk Overview
    const riskChartCtx = document.getElementById('riskChart');
    if (riskChartCtx && typeof Chart !== 'undefined') {
        const isDark = document.documentElement.classList.contains('dark');
        const textColor = isDark ? '#94a3b8' : '#64748b';
        
        window.myRiskChart = new Chart(riskChartCtx, {
            type: 'doughnut',
            data: {
                labels: ['Low Risk', 'Medium Risk', 'High Risk', 'Critical'],
                datasets: [{
                    data: [0, 0, 0, 0], // Start empty, will be updated by loadDashboardData
                    backgroundColor: [
                        '#10b981', // green
                        '#f59e0b', // amber
                        '#ef4444', // red
                        '#7f1d1d'  // dark red
                    ],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: textColor,
                            font: {
                                family: "'Inter', sans-serif",
                                size: 12
                            },
                            usePointStyle: true,
                            padding: 20
                        }
                    }
                }
            }
        });
    }

    // Chat functionality (if present on dashboard)
    const chatInput = document.getElementById('chat-input-field');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');

    if (sendBtn && chatInput && chatMessages) {
        sendBtn.addEventListener('click', async () => {
            const msg = chatInput.value.trim();
            if (!msg) return;

            const userP = document.createElement('p');
            userP.innerHTML = `<strong>You:</strong> ${msg}`;
            chatMessages.appendChild(userP);
            chatInput.value = '';
            
            chatMessages.scrollTop = chatMessages.scrollHeight;

            try {
                // Determine which contract we are chatting about (from URL if present)
                const urlParams = new URLSearchParams(window.location.search);
                const contractId = urlParams.get('id') || 1; // fallback if on dashboard
                
                const response = await api.post('/chat', { contract_id: contractId, message: msg });
                
                const botP = document.createElement('p');
                botP.innerHTML = `<strong>Bot:</strong> ${response.reply || response.message || 'I received your message.'}`;
                chatMessages.appendChild(botP);
            } catch (err) {
                const botP = document.createElement('p');
                botP.innerHTML = `<strong>Error:</strong> Failed to get a response from AI.`;
                botP.classList.add('text-red-500');
                chatMessages.appendChild(botP);
            }
            
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
    }
});
