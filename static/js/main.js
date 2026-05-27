/**
 * AgriShield AI — Client-Side Controller
 * Handles tab switching, file upload, disease analysis, and chatbot interactions.
 */

// ═══════════════════════════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════════════════════════
const state = {
    currentTab: 'scanner',
    selectedFile: null,
    isAnalyzing: false,
    isChatting: false,
};

// ═══════════════════════════════════════════════════════════════════════════
// DOM REFERENCES
// ═══════════════════════════════════════════════════════════════════════════
const dom = {
    // Tabs
    tabScanner:       () => document.getElementById('tab-scanner'),
    tabChatbot:       () => document.getElementById('tab-chatbot'),
    panelScanner:     () => document.getElementById('panel-scanner'),
    panelChatbot:     () => document.getElementById('panel-chatbot'),

    // Scanner
    dropZone:         () => document.getElementById('drop-zone'),
    fileInput:        () => document.getElementById('file-input'),
    uploadPlaceholder:() => document.getElementById('upload-placeholder'),
    previewContainer: () => document.getElementById('image-preview-container'),
    imagePreview:     () => document.getElementById('image-preview'),
    fileName:         () => document.getElementById('file-name'),
    analyzeBtn:       () => document.getElementById('analyze-btn'),
    analyzeBtnText:   () => document.getElementById('analyze-btn-text'),
    analyzeSpinner:   () => document.getElementById('analyze-spinner'),
    resultsEmpty:     () => document.getElementById('results-empty'),
    resultsLoading:   () => document.getElementById('results-loading'),
    resultsContent:   () => document.getElementById('results-content'),

    // Chat
    chatMessages:     () => document.getElementById('chat-messages'),
    chatInput:        () => document.getElementById('chat-input'),
    chatForm:         () => document.getElementById('chat-form'),
    sendBtn:          () => document.getElementById('send-btn'),
    sendBtnText:      () => document.getElementById('send-btn-text'),
    sendSpinner:      () => document.getElementById('send-spinner'),
    typingIndicator:  () => document.getElementById('typing-indicator'),
};

// ═══════════════════════════════════════════════════════════════════════════
// TAB SWITCHING
// ═══════════════════════════════════════════════════════════════════════════
function switchTab(tab) {
    state.currentTab = tab;

    const scannerTab  = dom.tabScanner();
    const chatbotTab  = dom.tabChatbot();
    const scannerPanel = dom.panelScanner();
    const chatbotPanel = dom.panelChatbot();

    const activeClasses   = 'text-white bg-emerald-700 shadow-md';
    const inactiveClasses = 'text-slate-600 hover:text-emerald-700';

    if (tab === 'scanner') {
        scannerTab.className  = `tab-btn relative px-6 py-2.5 text-sm font-semibold rounded-lg transition-all duration-300 ${activeClasses}`;
        chatbotTab.className  = `tab-btn relative px-6 py-2.5 text-sm font-semibold rounded-lg transition-all duration-300 ${inactiveClasses}`;
        scannerPanel.classList.add('active');
        chatbotPanel.classList.remove('active');
    } else {
        chatbotTab.className  = `tab-btn relative px-6 py-2.5 text-sm font-semibold rounded-lg transition-all duration-300 ${activeClasses}`;
        scannerTab.className  = `tab-btn relative px-6 py-2.5 text-sm font-semibold rounded-lg transition-all duration-300 ${inactiveClasses}`;
        chatbotPanel.classList.add('active');
        scannerPanel.classList.remove('active');
        scrollChatToBottom();
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// DRAG & DROP + FILE INPUT
// ═══════════════════════════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {
    const dropZone  = dom.dropZone();
    const fileInput = dom.fileInput();

    // Drag events
    ['dragenter', 'dragover'].forEach(evt => {
        dropZone.addEventListener(evt, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('drag-over');
        });
    });

    ['dragleave', 'drop'].forEach(evt => {
        dropZone.addEventListener(evt, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('drag-over');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelection(files[0]);
        }
    });

    // Standard file input
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            handleFileSelection(fileInput.files[0]);
        }
    });
});

function handleFileSelection(file) {
    const allowed = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];

    if (!allowed.includes(file.type)) {
        showError('results', 'Unsupported file format. Please upload a PNG, JPG, JPEG, or WEBP image.');
        return;
    }

    if (file.size > 16 * 1024 * 1024) {
        showError('results', 'File exceeds the 16MB size limit.');
        return;
    }

    state.selectedFile = file;

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        dom.imagePreview().src = e.target.result;
        dom.fileName().textContent = file.name;
        dom.uploadPlaceholder().classList.add('hidden');
        dom.previewContainer().classList.remove('hidden');
    };
    reader.readAsDataURL(file);

    // Enable button
    dom.analyzeBtn().disabled = false;

    // Reset results to empty state
    dom.resultsEmpty().classList.remove('hidden');
    dom.resultsLoading().classList.add('hidden');
    dom.resultsContent().classList.add('hidden');
}

// ═══════════════════════════════════════════════════════════════════════════
// DISEASE ANALYSIS
// ═══════════════════════════════════════════════════════════════════════════
async function analyzeCrop() {
    if (state.isAnalyzing || !state.selectedFile) return;

    state.isAnalyzing = true;
    lockButton('analyze');

    // Show loading state in results
    dom.resultsEmpty().classList.add('hidden');
    dom.resultsContent().classList.add('hidden');
    dom.resultsLoading().classList.remove('hidden');

    try {
        const formData = new FormData();
        formData.append('image', state.selectedFile);

        const scanMode = document.getElementById('scan-mode').value;
        const endpoint = scanMode === 'fruit' ? '/api/analyze_fruit' : '/api/analyze';

        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        if (data.success) {
            renderDiagnosis(data.data);
        } else {
            showError('results', data.error || 'Analysis failed. Please try again.');
        }
    } catch (err) {
        showError('results', 'Network error: Unable to reach the analysis server. Please check your connection.');
    } finally {
        state.isAnalyzing = false;
        unlockButton('analyze');
    }
}

function renderDiagnosis(d) {
    const container = dom.resultsContent();

    // Determine status styling
    const statusMap = {
        'Healthy':             { color: 'emerald', icon: '✅', bg: 'bg-emerald-50', border: 'border-emerald-200', text: 'text-emerald-800' },
        'Diseased':            { color: 'red',     icon: '🔴', bg: 'bg-red-50',     border: 'border-red-200',     text: 'text-red-800' },
        'Pest Infestation':    { color: 'orange',  icon: '🐛', bg: 'bg-orange-50',  border: 'border-orange-200',  text: 'text-orange-800' },
        'Nutrient Deficiency': { color: 'amber',   icon: '⚠️', bg: 'bg-amber-50',   border: 'border-amber-200',   text: 'text-amber-800' },
        'Unknown':             { color: 'slate',   icon: '❓', bg: 'bg-slate-50',   border: 'border-slate-200',   text: 'text-slate-700' },
    };

    const status = statusMap[d.health_status] || statusMap['Unknown'];

    // Parse confidence value for the bar
    const confidenceNum = parseInt(d.confidence) || 0;

    container.innerHTML = `
        <!-- Status Banner -->
        <div class="${status.bg} ${status.border} border rounded-xl p-4 animate-slide-up">
            <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                    <span class="text-xl">${status.icon}</span>
                    <span class="text-sm font-bold ${status.text}">${d.health_status}</span>
                </div>
                <span class="text-xs font-medium text-slate-500 bg-white px-2.5 py-1 rounded-full border border-slate-100">
                    ${d.plant_type}
                </span>
            </div>
        </div>

        <!-- Diagnosis -->
        <div class="bg-white rounded-xl border border-slate-100 p-4 animate-slide-up" style="animation-delay: 0.1s;">
            <h4 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">Diagnosis</h4>
            <p class="text-sm font-semibold text-slate-800">${escapeHtml(d.diagnosis)}</p>
        </div>

        <!-- Confidence Meter -->
        <div class="bg-white rounded-xl border border-slate-100 p-4 animate-slide-up" style="animation-delay: 0.15s;">
            <div class="flex items-center justify-between mb-2">
                <h4 class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Confidence</h4>
                <span class="text-sm font-bold ${status.text}">${d.confidence}</span>
            </div>
            <div class="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden">
                <div class="confidence-bar h-full rounded-full bg-gradient-to-r from-emerald-400 to-emerald-600"
                     style="width: 0%;"
                     data-target="${confidenceNum}">
                </div>
            </div>
        </div>

        <!-- Symptoms -->
        ${d.symptoms && d.symptoms.length > 0 ? `
        <div class="bg-white rounded-xl border border-slate-100 p-4 animate-slide-up" style="animation-delay: 0.2s;">
            <h4 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Observed Symptoms</h4>
            <ul class="space-y-1.5">
                ${d.symptoms.map(s => `
                    <li class="flex items-start gap-2 text-sm text-slate-700">
                        <span class="w-1.5 h-1.5 rounded-full bg-red-400 mt-1.5 flex-shrink-0"></span>
                        ${escapeHtml(s)}
                    </li>
                `).join('')}
            </ul>
        </div>
        ` : ''}

        <!-- Medicine / Treatment -->
        ${d.medicine && d.medicine.length > 0 ? `
        <div class="bg-blue-50/60 rounded-xl border border-blue-100 p-4 animate-slide-up" style="animation-delay: 0.22s;">
            <h4 class="text-xs font-semibold text-blue-600 uppercase tracking-wider mb-2">Recommended Medicine / Treatment</h4>
            <ul class="space-y-2">
                ${d.medicine.map(m => `
                    <li class="flex items-start gap-2 text-sm text-blue-900">
                        <span class="text-blue-500 mt-0.5 flex-shrink-0">💊</span>
                        ${escapeHtml(m)}
                    </li>
                `).join('')}
            </ul>
        </div>
        ` : ''}

        <!-- Management Recommendations -->
        ${d.management && d.management.length > 0 ? `
        <div class="bg-emerald-50/60 rounded-xl border border-emerald-100 p-4 animate-slide-up" style="animation-delay: 0.25s;">
            <h4 class="text-xs font-semibold text-emerald-600 uppercase tracking-wider mb-2">Management Recommendations</h4>
            <ul class="space-y-2">
                ${d.management.map(m => `
                    <li class="flex items-start gap-2 text-sm text-emerald-900">
                        <span class="text-emerald-500 mt-0.5 flex-shrink-0">🌿</span>
                        ${escapeHtml(m)}
                    </li>
                `).join('')}
            </ul>
        </div>
        ` : ''}
    `;

    // Show results
    dom.resultsLoading().classList.add('hidden');
    dom.resultsContent().classList.remove('hidden');

    // Animate confidence bar
    requestAnimationFrame(() => {
        setTimeout(() => {
            const bar = container.querySelector('.confidence-bar');
            if (bar) {
                bar.style.width = bar.dataset.target + '%';
            }
        }, 100);
    });
}

function clearScan() {
    state.selectedFile = null;

    // Reset file input
    dom.fileInput().value = '';

    // Reset preview
    dom.uploadPlaceholder().classList.remove('hidden');
    dom.previewContainer().classList.add('hidden');
    dom.imagePreview().src = '';
    dom.fileName().textContent = '';

    // Disable button
    dom.analyzeBtn().disabled = true;

    // Reset results
    dom.resultsEmpty().classList.remove('hidden');
    dom.resultsLoading().classList.add('hidden');
    dom.resultsContent().classList.add('hidden');
    dom.resultsContent().innerHTML = '';
}

// ═══════════════════════════════════════════════════════════════════════════
// CHATBOT
// ═══════════════════════════════════════════════════════════════════════════
async function sendMessage(e) {
    e.preventDefault();

    const input = dom.chatInput();
    const message = input.value.trim();

    if (!message || state.isChatting) return;

    state.isChatting = true;
    lockButton('send');

    // Add user bubble
    appendChatBubble('user', message);
    input.value = '';

    // Show typing indicator
    dom.typingIndicator().classList.remove('hidden');
    scrollChatToBottom();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();

        // Hide typing
        dom.typingIndicator().classList.add('hidden');

        if (data.success) {
            appendChatBubble('ai', data.reply);
        } else {
            appendChatBubble('ai', `⚠️ ${data.error || 'Something went wrong. Please try again.'}`);
        }
    } catch (err) {
        dom.typingIndicator().classList.add('hidden');
        appendChatBubble('ai', '⚠️ Network error: Unable to reach the chat server. Please check your connection.');
    } finally {
        state.isChatting = false;
        unlockButton('send');
        input.focus();
    }
}

function appendChatBubble(role, text) {
    const container = dom.chatMessages();
    const wrapper = document.createElement('div');
    wrapper.className = `flex ${role === 'user' ? 'justify-end' : 'justify-start'}`;
    wrapper.style.opacity = '0';
    wrapper.style.transform = 'translateY(10px)';

    const bubble = document.createElement('div');
    bubble.className = role === 'user' ? 'chat-bubble-user px-4 py-3' : 'chat-bubble-ai px-4 py-3';

    // Format text with simple markdown-like rendering
    bubble.innerHTML = `<p class="text-sm leading-relaxed whitespace-pre-wrap">${formatChatText(text)}</p>`;

    wrapper.appendChild(bubble);
    container.appendChild(wrapper);

    // Animate in
    requestAnimationFrame(() => {
        wrapper.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        wrapper.style.opacity = '1';
        wrapper.style.transform = 'translateY(0)';
    });

    scrollChatToBottom();
}

function formatChatText(text) {
    // Escape HTML first
    let safe = escapeHtml(text);
    // Bold: **text**
    safe = safe.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    // Italic: *text*
    safe = safe.replace(/\*(.+?)\*/g, '<em>$1</em>');
    // Bullet points: lines starting with - or •
    safe = safe.replace(/^[\-•]\s+/gm, '&#8226; ');
    return safe;
}

async function clearChat() {
    try {
        await fetch('/api/chat/clear', { method: 'POST' });
    } catch (err) {
        // Ignore network errors on clear
    }

    // Reset UI
    const container = dom.chatMessages();
    container.innerHTML = `
        <div class="flex justify-start">
            <div class="chat-bubble-ai px-4 py-3">
                <p class="text-sm leading-relaxed">
                    👋 <strong>Hello!</strong> I'm your AgriShield AI Advisor — a virtual senior agronomist here to help you with soil management, irrigation, pest control, crop rotation, and all things farming. How can I assist you today?
                </p>
            </div>
        </div>
    `;
}

// ═══════════════════════════════════════════════════════════════════════════
// UTILITY FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════
function scrollChatToBottom() {
    const messages = dom.chatMessages();
    requestAnimationFrame(() => {
        messages.scrollTop = messages.scrollHeight;
    });
}

function lockButton(type) {
    if (type === 'analyze') {
        dom.analyzeBtn().disabled = true;
        dom.analyzeBtnText().textContent = 'Analyzing…';
        dom.analyzeSpinner().classList.remove('hidden');
    } else if (type === 'send') {
        dom.sendBtn().disabled = true;
        dom.sendBtnText().textContent = 'Sending…';
        dom.sendSpinner().classList.remove('hidden');
    }
}

function unlockButton(type) {
    if (type === 'analyze') {
        dom.analyzeBtn().disabled = !state.selectedFile;
        dom.analyzeBtnText().textContent = 'Analyze Disease';
        dom.analyzeSpinner().classList.add('hidden');
    } else if (type === 'send') {
        dom.sendBtn().disabled = false;
        dom.sendBtnText().textContent = 'Send';
        dom.sendSpinner().classList.add('hidden');
    }
}

function showError(target, message) {
    if (target === 'results') {
        const container = dom.resultsContent();
        container.innerHTML = `
            <div class="bg-red-50 border border-red-200 rounded-xl p-4 animate-slide-up">
                <div class="flex items-start gap-3">
                    <svg class="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"/>
                    </svg>
                    <div>
                        <p class="text-sm font-semibold text-red-800">Analysis Error</p>
                        <p class="text-xs text-red-600 mt-1">${escapeHtml(message)}</p>
                    </div>
                </div>
            </div>
        `;
        dom.resultsLoading().classList.add('hidden');
        dom.resultsEmpty().classList.add('hidden');
        dom.resultsContent().classList.remove('hidden');
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
