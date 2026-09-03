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
    const contractsList = document.getElementById('contracts-list');

    if (totalContracts && pendingReviews) {
        // Mock data
        totalContracts.textContent = '12';
        pendingReviews.textContent = '3';

        const mockContracts = [
            { id: 1, name: 'Vendor_Agreement_2024.pdf', status: 'Analyzed' },
            { id: 2, name: 'NDA_AcmeCorp.docx', status: 'Pending Review' }
        ];

        if (contractsList) {
            contractsList.innerHTML = mockContracts.map(c => 
                `<li>
                    <span>${c.name}</span>
                    <span class="badge ${c.status === 'Analyzed' ? 'success' : 'warning'}">${c.status}</span>
                </li>`
            ).join('');
        }
    }

    // Chat functionality
    const chatInput = document.getElementById('chat-input-field');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');

    if (sendBtn && chatInput && chatMessages) {
        sendBtn.addEventListener('click', () => {
            const msg = chatInput.value.trim();
            if (!msg) return;

            const userP = document.createElement('p');
            userP.innerHTML = `<strong>You:</strong> ${msg}`;
            chatMessages.appendChild(userP);
            chatInput.value = '';

            setTimeout(() => {
                const botP = document.createElement('p');
                botP.innerHTML = `<strong>Bot:</strong> I'm a demo bot. I can't analyze this yet!`;
                chatMessages.appendChild(botP);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 1000);
        });
    }
});
