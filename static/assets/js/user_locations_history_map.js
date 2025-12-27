document.addEventListener('DOMContentLoaded', function() {
    const map = L.map('history-map').setView([15.281361, 66.547169], 5);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    const markersGroup = L.markerClusterGroup({
        iconCreateFunction: function(cluster) {
            const markers = cluster.getAllChildMarkers();
            const hasOnline = markers.some(m => m.options.icon.options.color === 'green');
            const hasOffline = markers.some(m => m.options.icon.options.color === 'grey');
            
            let className = '';
            if (hasOnline && hasOffline) {
                className = 'marker-cluster-mixed';
            } else if (hasOnline) {
                className = 'marker-cluster-green';
            } else {
                className = 'marker-cluster-grey';
            }

            return L.divIcon({
                html: `<span>${cluster.getChildCount()}</span>`,
                className: className,
                iconSize: L.point(40, 40)
            });
        }
    });

    const offlineIcon = L.icon({
        iconUrl: '/static/assets/img/leaflet-icons/marker-icon-grey.png',
        shadowUrl: '/static/assets/img/leaflet-icons/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41],
        color: 'grey'
    });

    const noResultsMessage = document.getElementById('no-results-message');

    async function fetchHistory() {
        const userId = document.getElementById('user-select').value;
        const from = document.getElementById('from-date').value;
        const to = document.getElementById('to-date').value;

        let url = `/location/api/v1/cms/employee-locations-history/?`;
        if (userId) url += `user_id=${userId}&`;
        if (from) url += `start_date=${encodeURIComponent(from)}&`;
        if (to) url += `end_date=${encodeURIComponent(to)}&`;

        const response = await fetch(url, { credentials: 'same-origin' });
        const result = await response.json();

        const locations = Array.isArray(result.data) ? result.data : [];

        markersGroup.clearLayers();

        if (locations.length === 0) {
            noResultsMessage.classList.remove('d-none');
            return;
        } else {
            noResultsMessage.classList.add('d-none');
        }

        locations.forEach(user => {
            const lat = parseFloat(user.latitude);
            const lng = parseFloat(user.longitude);
            const marker = L.marker([lat, lng], { icon: offlineIcon })
                .bindPopup(`<strong>${user.username}</strong><br>${new Date(user.recorded_at).toLocaleString()}`);
            markersGroup.addLayer(marker);
        });

        map.addLayer(markersGroup);

        const group = new L.featureGroup(markersGroup.getLayers());
        map.fitBounds(group.getBounds().pad(0.2));
    }

    document.getElementById('filter-btn').addEventListener('click', fetchHistory);
});