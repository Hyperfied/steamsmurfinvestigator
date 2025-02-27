document.addEventListener("DOMContentLoaded", () => {
  const searchForm = document.getElementById("searchForm");
  const searchInput = document.getElementById("searchInput");
  const messageDiv = document.getElementById("message");
  const profileNameDiv = document.querySelector(".profile-name");
  const profilePictureDiv = document.querySelector(".profile-picture");
  const recentSearchesContainer = document.querySelector(".recent-searches");

  const darkModeToggle = document.getElementById("darkModeToggle");

  darkModeToggle.addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");
  });

  searchForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const steamId = searchInput.value.trim();

    // Clear previous messages
    messageDiv.textContent = "";

    if (!steamId) {
      messageDiv.textContent = "Please enter a Steam ID.";
      return;
    }

    // Replace YOUR_API_KEY with actual Steam API key
    const proxyUrl = "http://localhost:8080/proxy"; // Free CORS proxy
    const apiKey = "";
    const url = `${proxyUrl}/ISteamUser/GetPlayerSummaries/v0002/?key=${apiKey}&steamids=${steamId}`;

    try {
      const response = await fetch(url);

      if (!response.ok) {
        messageDiv.textContent = `Network error: ${response.statusText}`;
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      console.log("Steam API Response:", data);

      if (data?.response?.players?.length > 0) {
        const player = data.response.players[0];

        // Update profile details
        profileNameDiv.textContent = player.personaname;
        profilePictureDiv.innerHTML = `<img src="${player.avatarfull}" alt="Profile Picture" style="width: 100%; height: 100%; object-fit: cover;" />`;
        messageDiv.textContent = "Profile loaded successfully.";
        messageDiv.style.color = "green";

        // Create a new recent search entry
        const recentSearchItem = document.createElement("div");
        recentSearchItem.classList.add("recent-search-item");
        recentSearchItem.innerHTML = `
          <img src="${player.avatarfull}" alt="${player.personaname}" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 8px; vertical-align: middle;">
          <span style="vertical-align: middle;">${player.personaname}</span>
        `;
        // Append the new entry to recent searches (it stays until the page is closed)
        recentSearchesContainer.appendChild(recentSearchItem);
      } else {
        messageDiv.textContent = "No player found with this Steam ID.";
        profileNameDiv.textContent = "Profile Name";
        profilePictureDiv.textContent = "Profile Picture";
        messageDiv.style.color = "red";
      }
    } catch (error) {
      console.error("Error fetching Steam profile:", error);
      messageDiv.textContent = "Error fetching Steam profile.";
      messageDiv.style.color = "red";
    }

    // Clear the input after processing
    searchInput.value = "";
  });
});