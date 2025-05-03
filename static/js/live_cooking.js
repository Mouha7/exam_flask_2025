document.addEventListener("DOMContentLoaded", function () {
	// Connexion au serveur Socket.IO
	const socket = io();

	// Écouter les événements de cuisine
	socket.on("cooking_started", function (data) {
		// Créer une notification avec un design amélioré
		const notif = document.createElement("div");
		notif.className =
			"p-4 rounded-md shadow-md relative bg-blue-50 text-blue-800 border-l-4 border-blue-400 animate-slide-in";
		notif.innerHTML = `
            <div class="flex items-start">
                <i class="bi bi-fire text-blue-500 text-lg mr-3 mt-0.5"></i>
                <div class="flex-1">
                    <p class="font-medium">Nouvelle activité culinaire</p>
                    <p class="text-sm mt-0.5">
                        <span class="font-semibold capitalize">${data.user}</span> a commencé à cuisiner 
                        <a href="/recipe/${data.recipe_id}" class="text-blue-600 hover:underline font-medium">${data.recipe_title}</a>
                    </p>
                </div>
                <button type="button" class="text-gray-400 hover:text-gray-600 focus:outline-none" onclick="this.parentElement.parentElement.remove()">
                    <i class="bi bi-x text-lg"></i>
                </button>
            </div>
        `;

		// Ajouter la notification et la supprimer après 5 secondes
		const notificationsContainer = document.getElementById("notifications");
		if (notificationsContainer) {
			notificationsContainer.prepend(notif);

			// Jouer le son
			playNotificationSound();

			setTimeout(function () {
				notif.classList.remove("animate-slide-in");
				notif.classList.add("animate-fade-out");
				setTimeout(function () {
					notif.remove();
				}, 500);
			}, 5000);
		}
	});

	socket.on("cooking_stopped", function (data) {
		// Créer une notification avec un design amélioré
		const notif = document.createElement("div");
		notif.className =
			"p-4 rounded-md shadow-md relative bg-yellow-50 text-yellow-800 border-l-4 border-yellow-400 animate-slide-in";
		notif.innerHTML = `
            <div class="flex items-start">
                <i class="bi bi-stop-circle text-yellow-500 text-lg mr-3 mt-0.5"></i>
                <div class="flex-1">
                    <p class="font-medium">Fin d'activité culinaire</p>
                    <p class="text-sm mt-0.5">
                        <span class="font-semibold capitalize">${data.user}</span> a terminé de cuisiner 
                        <a href="/recipe/${data.recipe_id}" class="text-yellow-700 hover:underline font-medium">${data.recipe_title}</a>
                    </p>
                </div>
                <button type="button" class="text-gray-400 hover:text-gray-600 focus:outline-none" onclick="this.parentElement.parentElement.remove()">
                    <i class="bi bi-x text-lg"></i>
                </button>
            </div>
        `;

		// Ajouter la notification à la page
		const notificationsContainer = document.getElementById("notifications");
		if (notificationsContainer) {
			notificationsContainer.prepend(notif);

			// Jouer un son de notification
			playNotificationSound();

			// Supprimer automatiquement après 5 secondes
			setTimeout(function () {
				notif.classList.remove("animate-slide-in");
				notif.classList.add("animate-fade-out");
				setTimeout(function () {
					notif.remove();
				}, 500);
			}, 5000);
		}

		// Mettre à jour la liste des cuisiniers si on est sur la page de cuisine en direct
		const liveList = document.getElementById("live-cooking-list");
		if (liveList) {
			updateLiveCookingList();
		}
	});

	// Fonction pour jouer un son de notification
	function playNotificationSound() {
		try {
			const audio = new Audio("/static/sounds/notification.mp3");
			audio.volume = 0.5;
			audio
				.play()
				.catch((e) => console.log("Erreur de lecture audio:", e));
		} catch (error) {
			console.log("Son de notification non disponible. ", error);
		}
	}

	// Mettre à jour la liste des cuisiniers avec un design amélioré
	function updateLiveCookingList() {
		fetch("/api/live-cooking")
			.then((response) => response.json())
			.then((data) => {
				const liveList = document.getElementById("live-cooking-list");
				if (!liveList) return;

				liveList.innerHTML = "";

				if (data.length === 0) {
					liveList.innerHTML = `
                        <div class="col-span-full bg-white rounded-lg shadow-md p-8 text-center">
                            <div class="mb-4">
                                <svg class="mx-auto h-16 w-16 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                                </svg>
                            </div>
                            <p class="text-gray-500 mb-4">Personne ne cuisine pour le moment...</p>
                            <a href="/recipes" class="inline-block px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors">
                                <i class="bi bi-search mr-1"></i>
                                Trouver une recette à cuisiner
                            </a>
                        </div>
                    `;
					return;
				}

				data.forEach((cook) => {
					const cookItem = document.createElement("div");
					cookItem.className =
						"bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1";
					cookItem.innerHTML = `
                        <div class="p-5">
                            <h5 class="text-xl font-semibold mb-3 flex items-center capitalize">
                                <i class="bi bi-person-circle mr-2 text-blue-600"></i>
                                ${cook.user}
                            </h5>
                            <div class="bg-blue-50 rounded-md p-3 mb-4">
                                <p class="text-gray-700 flex items-start">
                                    <i class="bi bi-fire mr-2 text-red-500 mt-1"></i>
                                    <span>
                                        <span class="text-sm text-gray-500">Cuisine actuellement:</span><br>
                                        <a href="/recipe/${cook.recipe_id}" class="text-blue-600 hover:underline font-medium">
                                            ${cook.recipe_title}
                                        </a>
                                    </span>
                                </p>
                            </div>
                            <div class="flex justify-center items-center space-x-3">
                                <div class="animate-pulse h-3 w-3 rounded-full bg-red-500"></div>
                                <div class="animate-pulse delay-75 h-3 w-3 rounded-full bg-yellow-500"></div>
                                <div class="animate-pulse delay-150 h-3 w-3 rounded-full bg-green-500"></div>
                            </div>
                        </div>
                    `;
					liveList.appendChild(cookItem);
				});
			})
			.catch((error) => {
				console.error(
					"Erreur lors de la mise à jour des cuisiniers:",
					error
				);
			});
	}

	// Si on est sur la page de cuisine en direct, mettre à jour immédiatement et toutes les 15 secondes
	const liveList = document.getElementById("live-cooking-list");
	if (liveList) {
		// Mise à jour initiale
		updateLiveCookingList();
		// Mise à jour périodique
		setInterval(updateLiveCookingList, 5000);
	}
});
