document.addEventListener('DOMContentLoaded', function() {
    const map = L.map('history-map').setView([15.281361, 66.547169], 5);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    // Layer group to hold all history paths, stops, and markers
    const historyLayers = L.featureGroup().addTo(map);

    const noResultsMessage = document.getElementById('no-results-message');

    // Palette of vibrant colors for multiple users
    const userColors = [
        '#2563eb', // Blue
        '#7c3aed', // Purple
        '#059669', // Emerald
        '#ea580c', // Orange
        '#db2777', // Pink
        '#0891b2', // Cyan
        '#d97706', // Amber
    ];

    // Helper: Haversine distance in meters
    function getDistanceMeters(lat1, lon1, lat2, lon2) {
        const R = 6371e3; // Earth radius in meters
        const rad = Math.PI / 180;
        const dLat = (lat2 - lat1) * rad;
        const dLon = (lon2 - lon1) * rad;
        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                  Math.cos(lat1 * rad) * Math.cos(lat2 * rad) *
                  Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }

    // Helper: Format DateTime for display
    function formatDateTime(dateStr) {
        if (!dateStr) return '';
        const d = new Date(dateStr);
        return d.toLocaleString(undefined, {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }

    function formatTime(d) {
        if (!d) return '';
        return d.toLocaleTimeString(undefined, {
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    // Custom DivIcons for Start, End, and Stop
    function createCustomIcon(type) {
        let bg = '#10b981';
        let svg = '';
        let title = '';

        if (type === 'start') {
            bg = '#10b981'; // Green
            title = 'Start';
            svg = `<svg width="14" height="14" viewBox="0 0 24 24" fill="white"><polygon points="6,4 20,12 6,20"/></svg>`;
        } else if (type === 'end') {
            bg = '#ef4444'; // Red
            title = 'End';
            svg = `<svg width="12" height="12" viewBox="0 0 24 24" fill="white"><rect x="4" y="4" width="16" height="16" rx="2"/></svg>`;
        } else if (type === 'stop') {
            bg = '#f59e0b'; // Amber
            title = 'Stop';
            svg = `<svg width="14" height="14" viewBox="0 0 24 24" fill="white"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>`;
        }

        return L.divIcon({
            className: 'history-custom-marker',
            html: `
                <div style="
                    background: ${bg};
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border: 2.5px solid #ffffff;
                    box-shadow: 0 3px 8px rgba(0,0,0,0.35);
                    cursor: pointer;
                " title="${title}">
                    ${svg}
                </div>
            `,
            iconSize: [32, 32],
            iconAnchor: [16, 16],
            popupAnchor: [0, -18]
        });
    }

    // Stop detection algorithm (stays within maxDistanceMeters for at least minDurationMinutes)
    function detectStops(points, maxDistanceMeters = 35, minDurationMinutes = 5) {
        if (points.length < 2) return [];

        const stops = [];
        let cluster = [points[0]];

        for (let i = 1; i < points.length; i++) {
            const pt = points[i];
            const firstPt = cluster[0];
            const dist = getDistanceMeters(firstPt.latitude, firstPt.longitude, pt.latitude, pt.longitude);

            if (dist <= maxDistanceMeters) {
                cluster.push(pt);
            } else {
                const startTime = new Date(cluster[0].recorded_at);
                const endTime = new Date(cluster[cluster.length - 1].recorded_at);
                const durationMinutes = (endTime - startTime) / (1000 * 60);

                if (durationMinutes >= minDurationMinutes) {
                    const avgLat = cluster.reduce((sum, p) => sum + p.latitude, 0) / cluster.length;
                    const avgLng = cluster.reduce((sum, p) => sum + p.longitude, 0) / cluster.length;

                    stops.push({
                        latitude: avgLat,
                        longitude: avgLng,
                        startTime: startTime,
                        endTime: endTime,
                        durationMinutes: Math.round(durationMinutes)
                    });
                }

                cluster = [pt];
            }
        }

        if (cluster.length > 1) {
            const startTime = new Date(cluster[0].recorded_at);
            const endTime = new Date(cluster[cluster.length - 1].recorded_at);
            const durationMinutes = (endTime - startTime) / (1000 * 60);

            if (durationMinutes >= minDurationMinutes) {
                const avgLat = cluster.reduce((sum, p) => sum + p.latitude, 0) / cluster.length;
                const avgLng = cluster.reduce((sum, p) => sum + p.longitude, 0) / cluster.length;

                stops.push({
                    latitude: avgLat,
                    longitude: avgLng,
                    startTime: startTime,
                    endTime: endTime,
                    durationMinutes: Math.round(durationMinutes)
                });
            }
        }

        return stops;
    }

    async function fetchHistory() {
        const userId = document.getElementById('user-select').value;
        const from = document.getElementById('from-date').value;
        const to = document.getElementById('to-date').value;

        let url = `/location/api/v1/cms/employee-locations-history/?`;
        if (userId) url += `user_id=${userId}&`;
        if (from) url += `start_date=${encodeURIComponent(from)}&`;
        if (to) url += `end_date=${encodeURIComponent(to)}&`;

        try {
            const response = await fetch(url, { credentials: 'same-origin' });
            const result = await response.json();
            const locations = Array.isArray(result.data) ? result.data : [];

            historyLayers.clearLayers();

            if (locations.length === 0) {
                if (noResultsMessage) noResultsMessage.classList.remove('d-none');
                return;
            } else {
                if (noResultsMessage) noResultsMessage.classList.add('d-none');
            }

            // Group points by user
            const userTracks = {};
            locations.forEach(loc => {
                if (!userTracks[loc.user_id]) {
                    userTracks[loc.user_id] = {
                        userId: loc.user_id,
                        username: loc.username,
                        points: []
                    };
                }
                userTracks[loc.user_id].points.push(loc);
            });

            const userKeys = Object.keys(userTracks);

            userKeys.forEach((uid, index) => {
                const track = userTracks[uid];
                // Ensure sorted chronologically
                track.points.sort((a, b) => new Date(a.recorded_at) - new Date(b.recorded_at));

                const color = userColors[index % userColors.length];
                const points = track.points;
                const latlngs = points.map(p => [p.latitude, p.longitude]);

                // Calculate total distance in km
                let totalDistanceMeters = 0;
                for (let i = 1; i < points.length; i++) {
                    totalDistanceMeters += getDistanceMeters(
                        points[i - 1].latitude, points[i - 1].longitude,
                        points[i].latitude, points[i].longitude
                    );
                }
                const totalDistanceKm = (totalDistanceMeters / 1000).toFixed(2);

                if (points.length >= 2) {
                    // 1. Draw Polyline
                    const polyline = L.polyline(latlngs, {
                        color: color,
                        weight: 4.5,
                        opacity: 0.85,
                        lineJoin: 'round'
                    }).addTo(historyLayers);

                    polyline.bindPopup(`
                        <div style="font-family: inherit; font-size: 13px; line-height: 1.5;">
                            <strong style="color: ${color}; font-size: 14px;">${track.username}</strong><br>
                            <b>المسافة التقديرية:</b> ${totalDistanceKm} كم<br>
                            <b>إجمالي النقاط:</b> ${points.length}<br>
                            <b>الفترة:</b> ${formatDateTime(points[0].recorded_at)} &larr; ${formatDateTime(points[points.length - 1].recorded_at)}
                        </div>
                    `);

                    // 2. Start Marker (🟢)
                    const firstPt = points[0];
                    const startMarker = L.marker([firstPt.latitude, firstPt.longitude], {
                        icon: createCustomIcon('start')
                    }).addTo(historyLayers);

                    startMarker.bindPopup(`
                        <div style="font-family: inherit; font-size: 13px; line-height: 1.5;">
                            <span class="badge" style="background:#10b981; color:white; font-size:12px; margin-bottom:5px;">🟢 نقطة البداية (Start)</span><br>
                            <b>الموظف:</b> ${track.username}<br>
                            <b>وقت البداية:</b> ${formatDateTime(firstPt.recorded_at)}
                        </div>
                    `);

                    // 3. End Marker (🔴)
                    const lastPt = points[points.length - 1];
                    const endMarker = L.marker([lastPt.latitude, lastPt.longitude], {
                        icon: createCustomIcon('end')
                    }).addTo(historyLayers);

                    endMarker.bindPopup(`
                        <div style="font-family: inherit; font-size: 13px; line-height: 1.5;">
                            <span class="badge" style="background:#ef4444; color:white; font-size:12px; margin-bottom:5px;">🔴 آخر موقع / النهاية (End)</span><br>
                            <b>الموظف:</b> ${track.username}<br>
                            <b>وقت النهاية:</b> ${formatDateTime(lastPt.recorded_at)}<br>
                            <b>إجمالي المسافة:</b> ${totalDistanceKm} كم
                        </div>
                    `);

                    // 4. Stop Markers (⏸️) - stops lasting >= 5 minutes
                    const stops = detectStops(points, 35, 5);
                    stops.forEach((stop, stopIdx) => {
                        // Skip if virtually identical to start or end marker to avoid overlapping
                        const distFromStart = getDistanceMeters(stop.latitude, stop.longitude, firstPt.latitude, firstPt.longitude);
                        const distFromEnd = getDistanceMeters(stop.latitude, stop.longitude, lastPt.latitude, lastPt.longitude);

                        if (distFromStart < 25) {
                            startMarker.setPopupContent(`
                                <div style="font-family: inherit; font-size: 13px; line-height: 1.5;">
                                    <span class="badge" style="background:#10b981; color:white; font-size:12px; margin-bottom:5px;">🟢 نقطة البداية (Start)</span><br>
                                    <b>الموظف:</b> ${track.username}<br>
                                    <b>وقت البداية:</b> ${formatDateTime(firstPt.recorded_at)}<br>
                                    <span style="color:#d97706; font-weight:bold;">⏸️ توقف هنا: ${stop.durationMinutes} دقيقة</span>
                                </div>
                            `);
                            return;
                        }

                        if (distFromEnd < 25) {
                            endMarker.setPopupContent(`
                                <div style="font-family: inherit; font-size: 13px; line-height: 1.5;">
                                    <span class="badge" style="background:#ef4444; color:white; font-size:12px; margin-bottom:5px;">🔴 آخر موقع / النهاية (End)</span><br>
                                    <b>الموظف:</b> ${track.username}<br>
                                    <b>وقت النهاية:</b> ${formatDateTime(lastPt.recorded_at)}<br>
                                    <span style="color:#d97706; font-weight:bold;">⏸️ توقف هنا: ${stop.durationMinutes} دقيقة</span><br>
                                    <b>إجمالي المسافة:</b> ${totalDistanceKm} كم
                                </div>
                            `);
                            return;
                        }

                        const stopMarker = L.marker([stop.latitude, stop.longitude], {
                            icon: createCustomIcon('stop')
                        }).addTo(historyLayers);

                        stopMarker.bindPopup(`
                            <div style="font-family: inherit; font-size: 13px; line-height: 1.5;">
                                <span class="badge" style="background:#f59e0b; color:white; font-size:12px; margin-bottom:5px;">⏸️ مكان توقف #${stopIdx + 1}</span><br>
                                <b>الموظف:</b> ${track.username}<br>
                                <b style="color: #b45309; font-size: 13px;">مدة التوقف: ${stop.durationMinutes} دقيقة</b><br>
                                <b>من:</b> ${formatTime(stop.startTime)}<br>
                                <b>إلى:</b> ${formatTime(stop.endTime)}
                            </div>
                        `);
                    });

                } else if (points.length === 1) {
                    const pt = points[0];
                    const singleMarker = L.marker([pt.latitude, pt.longitude], {
                        icon: createCustomIcon('start')
                    }).addTo(historyLayers);

                    singleMarker.bindPopup(`
                        <div style="font-family: inherit; font-size: 13px; line-height: 1.5;">
                            <b>الموظف:</b> ${track.username}<br>
                            <b>الموقع:</b> ${formatDateTime(pt.recorded_at)}
                        </div>
                    `);
                }
            });

            // Adjust map view to fit the route
            if (historyLayers.getLayers().length > 0) {
                map.fitBounds(historyLayers.getBounds().pad(0.15));
            }

        } catch (err) {
            console.error('Error fetching history:', err);
        }
    }

    const filterBtn = document.getElementById('filter-btn');
    if (filterBtn) {
        filterBtn.addEventListener('click', fetchHistory);
    }
});