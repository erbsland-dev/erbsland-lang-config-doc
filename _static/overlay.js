/*
 * Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
 * SPDX-License-Identifier: Apache-2.0
 */

function showOverlay(char, unicode_name, unicode_category, code_point, utf8_bytes) {
    // Create the overlay and content
    const overlay = document.createElement('div');
    overlay.className = 'cp-overlay';
    overlay.innerHTML = `
        <div class="content">
            <table class="cp-table">
                <tr><td class="cp-char" colspan="2">${char}</td></tr>
                <tr><td class="cp-label">Name:</td><td>${unicode_name}</td></tr>
                <tr><td class="cp-label">Category:</td><td>${unicode_category}</td></tr>
                <tr><td class="cp-label">Code Point:</td><td>${code_point}</td></tr>
                <tr><td class="cp-label">UTF-8 Bytes:</td><td>${utf8_bytes}</td></tr>
            </table>
            <button class="close-button" onclick="closeOverlay()">Close</button>
        </div>
    `;
    overlay.addEventListener('click', (e) => {
        closeOverlay();
    })

    // Add the overlay to the document
    document.body.appendChild(overlay);
}

function closeOverlay() {
    const overlay = document.querySelector('.cp-overlay');
    if (overlay) {
        overlay.remove();
    }
}