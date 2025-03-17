
const serverURL = "http://localhost:8000";

function updateSmurfBar(percentage) {
  const smurfBarFill = document.querySelector(".smurf-bar-fill");
  const smurfAnswer = document.querySelector(".smurf-answer");
  const bottomSection = document.querySelector(".bottom-section");

  // Ensure percentage is between 0 and 100
  percentage = Math.max(0, Math.min(100, percentage));

  // Update the width of the bar
  smurfBarFill.style.width = percentage + "%";

  // Change color based on percentage
  if (percentage >= 80) {
    smurfBarFill.style.background = "red";  // High risk (Smurf detected)
    smurfAnswer.style.background = "#ff6257";
    smurfAnswer.textContent = "Yes";
  } 
  else if (percentage >= 55 && percentage < 80)
  {
    smurfBarFill.style.background = "orange";  // High risk (Smurf detected)
    smurfAnswer.style.background = "#ffba3b";
    smurfAnswer.textContent = "No";
  }
  else {
    smurfBarFill.style.background = "green"; // Low risk (Not a smurf)
    smurfAnswer.style.background = "#ff6257";
    smurfAnswer.textContent = "No";
  }

  // Ensure the section is visible
  bottomSection.classList.add("show");
}

document.addEventListener("DOMContentLoaded", () => {
  const searchForm = document.getElementById("searchForm");
  const searchInput = document.getElementById("searchInput");
  const messageDiv = document.getElementById("message");
  const profileNameDiv = document.querySelector(".profile-name");
  const profilePictureDiv = document.querySelector(".profile-picture");
  const recentSearchesContainer = document.querySelector(".recent-searches");

  const smurfCalcSection = document.querySelector(".smurf-calc");
  const bottomSectionSection = document.querySelector(".bottom-section");

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

    if (steamId) {
      // Add 'show' class to smoothly reveal the section
      smurfCalcSection.classList.add("show");
      bottomSectionSection.classList.add("show");
    }

    // Use our server endpoints
    const url = `${serverURL}/profile/${steamId}`;

    try {
      const response = await fetch(url);

      if (!response.ok) {
        messageDiv.textContent = `Network error: ${response.statusText}`;
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      console.log("Backend API Response:", data);

      if (response.ok) {
        const personaname = data.personaName;
        const realName = data.realName;
        const avatar = data.avatar;
        const avatarFull = data.avatarFull;
        const avatarMedium = data.avatarMedium;

        updateSmurfBar(60);

        // Update profile details
        profileNameDiv.textContent = personaname;
        profilePictureDiv.innerHTML = `<img src="${avatarFull}" alt="Profile Picture" style="width: 100%; height: 100%; object-fit: cover;" />`;
        messageDiv.textContent = "Profile loaded successfully.";
        messageDiv.style.color = "green";

        // Create a new recent search entry
        const recentSearchItem = document.createElement("div");
        recentSearchItem.classList.add("recent-search-item");
        recentSearchItem.innerHTML = `
          <img src="${avatarFull}" alt="${personaname}" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 8px; vertical-align: middle;">
          <span style="vertical-align: middle;">${personaname}</span>
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