document.addEventListener('DOMContentLoaded', function() {
    // Connexion au serveur Socket.IO
    const socket = io();
    
    // Écouter les événements de cuisine
    socket.on('cooking_started', function(data) {
        // Créer une notification
        const notif = document.createElement('div');
        notif.className = 'alert alert-info';
        notif.innerHTML = `
            <div class="flex items-center">
                <i class="bi bi-fire mr-2 text-lg"></i>
                <div>
                    <span class="font-semibold">${data.user}</span> a commencé à cuisiner 
                    <a href="/recipe/${data.recipe_id}" class="text-blue-600 hover:underline">${data.recipe_title}</a>
                </div>
            </div>
            <button type="button" class="absolute top-2 right-2 text-gray-400 hover:text-gray-500" onclick="this.parentElement.remove()">
                <i class="bi bi-x"></i>
            </button>
        `;
        
        // Ajouter la notification et la supprimer après 5 secondes
        const notificationsContainer = document.getElementById('notifications');
        if (notificationsContainer) {
            notificationsContainer.prepend(notif);
            
            // Jouer le son
            playNotificationSound();
            
            setTimeout(function() {
                notif.classList.add('fade-out');
                setTimeout(function() {
                    notif.remove();
                }, 500);
            }, 5000);
        }
    });

    socket.on('cooking_stopped', function(data) {
        // Créer une notification
        const notif = document.createElement('div');
        notif.className = 'alert alert-warning';
        notif.innerHTML = `
            <div class="flex items-center">
                <i class="bi bi-stop-circle mr-2 text-lg"></i>
                <div>
                    <span class="font-semibold">${data.user}</span> a arrêté de cuisiner 
                    <a href="/recipe/${data.recipe_id}" class="text-blue-600 hover:underline">${data.recipe_title}</a>
                </div>
            </div>
            <button type="button" class="absolute top-2 right-2 text-gray-400 hover:text-gray-500" onclick="this.parentElement.remove()">
                <i class="bi bi-x"></i>
            </button>
        `;
        
        // Ajouter la notification à la page
        const notificationsContainer = document.getElementById('notifications');
        if (notificationsContainer) {
            notificationsContainer.prepend(notif);
            
            // Jouer un son de notification
            playNotificationSound();
            
            // Supprimer automatiquement après 5 secondes
            setTimeout(function() {
                notif.classList.add('fade-out');
                setTimeout(function() {
                    notif.remove();
                }, 500);
            }, 5000);
        }
        
        // Mettre à jour la liste des cuisiniers si on est sur la page de cuisine en direct
        const liveList = document.getElementById('live-cooking-list');
        if (liveList) {
            updateLiveCookingList();
        }
    });
    
    // Fonction pour jouer un son de notification
    function playNotificationSound() {
        try {
            const audio = new Audio('/static/sounds/notification.mp3');
            audio.volume = 0.5;
            audio.play().catch(e => console.log('Erreur de lecture audio:', e));
        } catch (error) {
            console.log('Son de notification non disponible. ', error);
        }
    }
    
    // Mettre à jour la liste des cuisiniers
    function updateLiveCookingList() {
        fetch('/api/live-cooking')
            .then(response => response.json())
            .then(data => {
                const liveList = document.getElementById('live-cooking-list');
                if (!liveList) return;
                
                liveList.innerHTML = '';
                
                if (data.length === 0) {
                    liveList.innerHTML = `
                        <div class="col-12 text-center">
                            <p class="text-muted">Personne ne cuisine pour le moment...</p>
                            <p>Soyez le premier à <a href="/recipes">choisir une recette</a> à cuisiner!</p>
                        </div>
                    `;
                    return;
                }
                
                data.forEach(cook => {
                    const cookItem = document.createElement('div');
                    cookItem.className = 'md:w-1/3 mb-4 px-2';
                    cookItem.innerHTML = `
                        <div class="bg-white rounded-lg shadow-md overflow-hidden transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
                            <div class="p-4">
                                <h5 class="text-lg font-medium mb-2 flex items-center">
                                    <i class="bi bi-person-circle mr-2"></i>${cook.user}
                                </h5>
                                <p class="text-gray-700 mb-3">
                                    <i class="bi bi-fire mr-2 text-red-500"></i>Cuisine actuellement : 
                                    <a href="/recipe/${cook.recipe_id}" class="text-primary-600 hover:underline">${cook.recipe_title}</a>
                                </p>
                                <div class="flex justify-center items-center mt-3 space-x-2">
                                    <div class="animate-pulse h-2 w-2 rounded-full bg-red-500"></div>
                                    <div class="animate-pulse h-2 w-2 rounded-full bg-yellow-500"></div>
                                    <div class="animate-pulse h-2 w-2 rounded-full bg-green-500"></div>
                                </div>
                            </div>
                        </div>
                    `;
                    liveList.appendChild(cookItem);
                });
            })
            .catch(error => {
                console.error('Erreur lors de la mise à jour des cuisiniers:', error);
            });
    }
    
    // Si on est sur la page de cuisine en direct, mettre à jour immédiatement et toutes les 15 secondes
    const liveList = document.getElementById('live-cooking-list');
    if (liveList) {
        // Mise à jour initiale
        updateLiveCookingList();
        // Mise à jour périodique
        setInterval(updateLiveCookingList, 15000);
    }
});