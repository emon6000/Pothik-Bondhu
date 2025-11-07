document.addEventListener("DOMContentLoaded", function() {

    const datalistOptions = document.querySelectorAll('#districts-list option');
    const ALL_DISTRICTS = Array.from(datalistOptions).map(opt => opt.value);
    console.log("Loaded " + ALL_DISTRICTS.length + " districts from HTML datalist.");

    var map = L.map('map').setView([23.6850, 90.3563], 7);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
    }).addTo(map);
    var routeLayer = null;

    var startInput = document.getElementById('start');
    var endInput = document.getElementById('end');
    var submitButton = document.getElementById('submit-btn');
    var resultsPanel = document.getElementById('results-panel');
    
    const aboutLink = document.getElementById('about-link');
    const contactLink = document.getElementById('contact-link');
    const aboutModal = document.getElementById('about-modal');
    const contactModal = document.getElementById('contact-modal');
    const closeButtons = document.querySelectorAll('.modal-close-btn');
    const modalOverlays = document.querySelectorAll('.modal-overlay');

    submitButton.addEventListener('click', function() {
        var startValue = startInput.value;
        var endValue = endInput.value;

        const isValidStart = ALL_DISTRICTS.some(d => d.toLowerCase() === startValue.toLowerCase());
        const isValidEnd = ALL_DISTRICTS.some(d => d.toLowerCase() === endValue.toLowerCase());

        if (!isValidStart || !isValidEnd) {
            alert("Invalid location. Please select a valid district from the suggestion list for both Start and End.");
            return; 
        }

        console.log("Sending to Django:", startValue, "to", endValue);
        resultsPanel.innerHTML = `
            <div class="loader-container">
                <div class="loader"></div>
                <p class="loader-text">Loading your route...It may take some moments</p>
            </div>
        `;
        
        var apiUrl = '/api/plan-journey/'; 
        var postData = {
            start: startValue,
            end: endValue
        };

        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') 
            },
            body: JSON.stringify(postData)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { 
                    throw new Error(err.error || 'Server error. Could not plan route.'); 
                });
            }
            return response.json();
        })
        .then(data => {
            console.log("Full journey data received:", data);

            if (data.error) {
                resultsPanel.innerHTML = `<p style="color: red;">${data.error}</p>`;
                return;
            }

            if (routeLayer) { map.removeLayer(routeLayer); }
            routeLayer = L.geoJSON(data.route_geometry, {
                style: { color: '#00aaff', weight: 6, opacity: 0.8 }
            }).addTo(map);
            map.fitBounds(routeLayer.getBounds());

            var distanceKm = (data.route_distance / 1000).toFixed(1);
            var durationHours = (data.route_duration / 3600).toFixed(1);

            let finalHtml = `
                <div class="route-summary">
                    <h3>Your Route Summary</h3>
                    <p><strong>Total Distance(By road):</strong> ${distanceKm} km</p>
                    <p><strong>Estimated Time(Covered the speed limit rules):</strong> ${durationHours} hours</p>
                </div>
            `;
            
            data.journey_steps.forEach(step => {
                let weatherHtml = "<ul><li>Weather data only shown for start and end.</li></ul>";
                if (step.weather) {
                    weatherHtml = `
                        <ul>
                            <li><strong>Temp:</strong> ${step.weather.temp}°C</li>
                            <li><strong>Feels Like:</strong> ${step.weather.feels_like}°C</li>
                            <li><strong>Conditions:</strong> ${step.weather.description}</li>
                        </ul>
                    `;
                }
                
                let sightsHtml = "No notable sights listed.";
                if (step.top_sights && step.top_sights.trim() && step.top_sights !== "N/A") {
                    sightsHtml = "<ul>";
                    step.top_sights.split(',').forEach(sight => {
                        sightsHtml += `<li>${sight.trim()}</li>`;
                    });
                    sightsHtml += "</ul>";
                }
                
                let foodHtml = "No famous foods listed.";
                if (step.famous_food && step.famous_food.trim() && step.famous_food !== "N/A") {
                    foodHtml = "<ul>";
                    step.famous_food.split(',').forEach(food => {
                        foodHtml += `<li>${food.trim()}</li>`;
                    });
                    foodHtml += "</ul>";
                }
                
                finalHtml += `
                    <details class="step-accordion">
                        <summary class="step-summary">
                            On your way through: <strong>${step.district}</strong> 
                            <span>(${(step.weather ? step.weather.temp + '°C' : '...')})</span>
                        </summary>
                        <div class="step-content">
                            <h4>Weather</h4>
                            ${weatherHtml}
                            <h4>Top Sights</h4>
                            ${sightsHtml}
                            <h4>Famous Food & Items</h4>
                            ${foodHtml}
                        </div>
                    </details>
                `;
            });
            resultsPanel.innerHTML = finalHtml;
        })
        .catch(error => {
            console.error('Error:', error);
            resultsPanel.innerHTML = `<p style="color: red;">An error occurred: ${error.message}</p>`;
        });
    });

    function openModal(modal) {
        modal.classList.remove('hidden');
        setTimeout(() => modal.classList.add('visible'), 10);
    }
    function closeModal(modal) {
        modal.classList.remove('visible');
        setTimeout(() => modal.classList.add('hidden'), 300);
    }
    aboutLink.addEventListener('click', function(e) { e.preventDefault(); openModal(aboutModal); });
    contactLink.addEventListener('click', function(e) { e.preventDefault(); openModal(contactModal); });
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            closeModal(button.closest('.modal-overlay'));
        });
    });
    modalOverlays.forEach(overlay => {
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) { closeModal(overlay); }
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

});