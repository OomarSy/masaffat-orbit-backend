document.addEventListener('DOMContentLoaded', function() {
    const map = L.map('user-locations-map').setView([15.281361, 66.547169], 5);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Marker Cluster group with correct icon logic
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


    window.userMarkers = {};
    let firstLoad = true;

    const onlineIcon = L.icon({
        iconUrl: '/static/assets/img/leaflet-icons/marker-icon-green.png',
        shadowUrl: '/static/assets/img/leaflet-icons/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41],
        color: 'green'
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

    async function fetchEmployLocations() {
        try {
            const response = await fetch('/location/api/v1/cms/employee-locations/', { credentials: 'same-origin' });
            if (!response.ok) return;

            const data = await response.json();
            if (data.errorno !== 0) return;

            markersGroup.clearLayers();
            window.userMarkers = {};

            data.data.forEach(user => {
                if (user.latitude && user.longitude) {
                    const lat = parseFloat(user.latitude);
                    const lng = parseFloat(user.longitude);
                    const icon = user.is_online ? onlineIcon : offlineIcon;

                    const marker = L.marker([lat, lng], { icon: icon })
                        .bindPopup(`<strong>${user.username}</strong><br>Last updated: ${new Date(user.updated_at).toLocaleString()}<br>Status: ${user.is_online ? 'Online' : 'Offline'}`);
                    
                    markersGroup.addLayer(marker);
                    window.userMarkers[user.user_id] = marker;
                }
            });

            map.addLayer(markersGroup);

            if (firstLoad && Object.keys(window.userMarkers).length > 0) {
                const group = new L.featureGroup(Object.values(window.userMarkers));
                map.fitBounds(group.getBounds().pad(0.2));
                firstLoad = false;
            }

        } catch (err) {
            console.error(err);
        }
    }

    fetchEmployLocations();
    setInterval(fetchEmployLocations, 5000);
});
