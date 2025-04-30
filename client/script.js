
const serverURL = "http://localhost:8000";

// DOM Elements

let recentSearchesContainer = null;

let recentSearches = [];

//
//
//

async function getVanityURL(steamid) {
  const response = await fetch(`${serverURL}/profile/vanityurl/${steamid}`);
  const data = await response.json();
  return data.steamid;
}

async function getSummary(steamid) {
  const response = await fetch(`${serverURL}/profile/summary/${steamid}`);
  const data = await response.json();
  return data;
}

async function getFriends(steamid) {
  const response = await fetch(`${serverURL}/profile/friends/${steamid}`);
  const data = await response.json();
  return data;
}

async function getBans(steamid) {
  const response = await fetch(`${serverURL}/profile/bans/${steamid}`);
  const data = await response.json();
  return data;
}

async function getRecentPlaytime(steamid) {
  const response = await fetch(`${serverURL}/profile/recent/${steamid}`);
  const data = await response.json();
  return data;
}

async function getGames(steamid) {
  const response = await fetch(`${serverURL}/profile/games/${steamid}`);
  const data = await response.json();
  return data;
}

async function getAccountValue(steamid) {
  const response = await fetch(`${serverURL}/profile/value/${steamid}`);
  const data = await response.json();
  return data;
}


// -----------------------------------------------------
// Functions to get scores from the API
// --------------------------------------

async function getAccountAgeScore(days) {
  const response = await fetch(`${serverURL}/smurf/accountAge/${days}`);
  const score = await response.json();
  return score;
}

async function getAccountGamesScore(numOfGames) {
  const response = await fetch(`${serverURL}/smurf/accountGames/${numOfGames}`);
  const score = await response.json();
  return score;
}

async function getAccountBansScore(numOfBans) {
  const response = await fetch(`${serverURL}/smurf/accountBans/${numOfBans}`);
  const score = await response.json();
  return score;
}

async function getTotalPlaytimeScore(hours) {
  const response = await fetch(`${serverURL}/smurf/totalPlaytime/${hours}`);
  const score = await response.json();
  return score;
}

async function getLast2WeeksScore(last2Weeks, average2Weeks) {
  const response = await fetch(`${serverURL}/smurf/last2Weeks/${last2Weeks}/${average2Weeks}`);
  const score = await response.json();
  return score;
}

async function getAccountValueScore(value) {
  const response = await fetch(`${serverURL}/smurf/accountValue/${value}`);
  const score = await response.json();
  return score;
}

async function getAccountFriendsScore(numOfFriends) {
  const response = await fetch(`${serverURL}/smurf/accountFriends/${numOfFriends}`);
  const score = await response.json();
  return score;
}

async function getAchievementPercentageScore(completed, total) {
  const response = await fetch(`${serverURL}/smurf/achievementPercentage/${completed}/${total}`);
  const score = await response.json();
  return score;
}

function formatAccountAge(seconds) {
  // Calculate years, days, hours from total seconds
  const years = Math.floor(seconds / (365 * 24 * 60 * 60));
  const days = Math.floor((seconds % (365 * 24 * 60 * 60)) / (24 * 60 * 60));
  const hours = Math.floor((seconds % (24 * 60 * 60)) / (60 * 60));

  if (years > 0) {
    // If at least 1 year, display years, days, hours
    return `${years} year${years > 1 ? "s" : ""}, ${days} day${days !== 1 ? "s" : ""}, ${hours} hour${hours !== 1 ? "s" : ""}`;
  } else if (days > 0) {
    // If less than a year but more than a day
    return `${days} day${days !== 1 ? "s" : ""}, ${hours} hour${hours !== 1 ? "s" : ""}`;
  } else {
    // If less than a day
    return `${hours} hour${hours !== 1 ? "s" : ""}`;
  }
}

function formatHours(hours) {
  // Use Math.ceil to round up to the next whole number
  return `${Math.ceil(hours)} hours`;
}

function formatPercentage(value) {
  // Round to 2 decimal places and add '%'
  return `${value.toFixed(2)}%`;
}

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
    smurfAnswer.style.background = "red";
    smurfAnswer.textContent = "Yes";
  } 
  else if (percentage >= 50 && percentage < 80)
  {
    smurfBarFill.style.background = "orange";  // High risk (Smurf detected)
    smurfAnswer.style.background = "#orange";
    smurfAnswer.textContent = "Likely";
  }
  else {
    smurfBarFill.style.background = "green"; // Low risk (Not a smurf)
    smurfAnswer.style.background = "green";
    smurfAnswer.textContent = "No";
  }

  // Ensure the section is visible
  bottomSection.classList.add("show");
}

function addRecentSearchDiv(steamId, personaname, avatarFull) {
  const recentSearchItem = document.createElement("div");
  recentSearchItem.classList.add("recent-search-item");
  recentSearchItem.innerHTML = `
    <img src="${avatarFull}" alt="${personaname}" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 8px; vertical-align: middle;">
    <span style="vertical-align: middle;">${personaname}</span>
  `;
  recentSearchItem.addEventListener("click", () => {
    // When clicked, fill the input with the Steam ID and trigger the search
    searchInput.value = steamId;
    searchForm.dispatchEvent(new Event("submit", {cancelable: true}));

  });
  // Append the new entry to recent searches (it stays until the page is closed)
  recentSearchesContainer.appendChild(recentSearchItem);
}

function updateRecentSearchesDisplay() {
  let recentSearchesHeader = document.createElement("div");
  recentSearchesHeader.classList.add("recent-searches-header");

  let recentSearchesClear = document.createElement("span");
  recentSearchesClear.textContent = "X";
  recentSearchesClear.style.cursor = "pointer";
  recentSearchesClear.addEventListener("click", () => {
    // Clear recent searches from local storage and the display
    if (confirm("Are you sure you want to clear recent searches?")) {
      recentSearches = [];
      localStorage.removeItem("recentSearches");
      updateRecentSearchesDisplay();
    }
  })

  let recentSearchesTitle = document.createElement("span");
  recentSearchesTitle.textContent = "Recent Searches";

  recentSearchesHeader.appendChild(recentSearchesTitle);
  recentSearchesHeader.appendChild(recentSearchesClear);

  recentSearchesContainer.innerHTML = ""; // Clear previous entries
  recentSearchesContainer.appendChild(recentSearchesHeader); // Add header to the container
  recentSearches.forEach(search => {
    addRecentSearchDiv(search.steamId, search.personaname, search.avatarFull);
  });

}

function addRecentSearch(steamId, personaname, avatarFull) {
  const newSearch = { steamId, personaname, avatarFull };
  
  // Check if the search already exists in the array
  const existingIndex = recentSearches.findIndex(search => search.steamId === steamId);
  if (existingIndex !== -1) {
    // If it exists, remove it from its current position
    recentSearches.splice(existingIndex, 1);
  }

  // Add the new search to the beginning of the array
  recentSearches.unshift(newSearch);

  // Limit the number of recent searches to 10
  if (recentSearches.length > 10) {
    recentSearches.pop(); // Remove the oldest search
  }

  // Update the recent searches display
  updateRecentSearchesDisplay();

  // Save the recent searches to local storage
  localStorage.setItem("recentSearches", JSON.stringify(recentSearches));
}

document.addEventListener("DOMContentLoaded", () => {
  const searchForm = document.getElementById("searchForm");
  const searchInput = document.getElementById("searchInput");
  const messageDiv = document.getElementById("message");
  const profileNameDiv = document.querySelector(".profile-name");
  const profilePictureDiv = document.querySelector(".profile-picture");
  recentSearchesContainer = document.querySelector(".recent-searches");
  const accountAgeDiv = document.querySelector(".account-age");
  const numberOfGamesDiv = document.querySelector(".number-of-games");
  const numberOfBansDiv = document.querySelector(".number-of-bans");
  const totalPlaytimeDiv = document.querySelector(".total-playtime");
  const totalRecentPlaytimeDiv = document.querySelector(".total-recent-playtime");
  const numberOfFriendsDiv = document.querySelector(".number-of-friends");
  const averageCompletionOfGamesDiv = document.querySelector(".average-completion-of-games");
  const smurfCalcSection = document.querySelector(".smurf-calc");
  const bottomSectionSection = document.querySelector(".bottom-section");

  const darkModeToggle = document.getElementById("darkModeToggle");

  recentSearches = JSON.parse(localStorage.getItem("recentSearches")) || [];
  updateRecentSearchesDisplay(); // Load recent searches from local storage

  darkModeToggle.addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");
  });

  searchForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const steamId = searchInput.value.trim();

    // Clear previous messages and inputs
    messageDiv.textContent = "";
    profileNameDiv.textContent = "";
    profilePictureDiv.innerHTML = "<div class='profile-picture'></div>";
    accountAgeDiv.textContent = "";
    numberOfGamesDiv.textContent = "";
    numberOfBansDiv.textContent = "";
    totalPlaytimeDiv.textContent = "";
    totalRecentPlaytimeDiv.textContent = "";
    numberOfFriendsDiv.textContent = "";
    averageCompletionOfGamesDiv.textContent = "";
  

    if (!steamId) {
      messageDiv.textContent = "Please enter a Steam ID.";
      return;
    }

    if (steamId) {
      // Add 'show' class to smoothly reveal the section
      smurfCalcSection.classList.add("show");
      bottomSectionSection.classList.add("show");
    }

    try {
      const newsteamid = await getVanityURL(steamId);

      // Summary Data
      const summary = await getSummary(newsteamid);

      const personaname = summary.personaName;
      const realName = summary.realName;
      const avatar = summary.avatar;
      const avatarFull = summary.avatarFull;
      const avatarMedium = summary.avatarMedium;
      const accountAgeSeconds = summary.accountAgeSeconds;

      // Update profile details
      profileNameDiv.textContent = personaname;
      profilePictureDiv.innerHTML = `<img src="${avatarFull}" alt="Profile Picture" style="width: 100%; height: 100%; object-fit: cover;" />`;
      messageDiv.textContent = "Profile loaded successfully.";
      messageDiv.style.color = "green";

      accountAgeDiv.textContent = formatAccountAge(accountAgeSeconds);

      // Friends Data
      const friends = await getFriends(newsteamid);

      const friendTotal = friends.friendTotal;
      const friendTimestamps = friends.friendTimestamps;

      numberOfFriendsDiv.textContent = friendTotal;

      // Bans Data
      const bans = await getBans(newsteamid);

      const banNumber = bans.banNumber;
      const currentlyVACBanned = bans.currentlyVACBanned;

      numberOfBansDiv.textContent = banNumber;

      // Recent Playtime Data
      const recentPlaytime = await getRecentPlaytime(newsteamid);

      const recentPlaytimeHours = recentPlaytime.recentPlaytimeHours;

      totalRecentPlaytimeDiv.textContent = formatHours(recentPlaytimeHours);

      // Games Data
      const games = await getGames(newsteamid);

      const numberOfGames = games.numberOfGames;
      const totalPlaytimeHours = games.totalPlaytimeHours;
      const averageRecentPlaytime = games.averageRecentPlaytime
      const achievementCompletionPercentage = games.achievementCompletionPercentage;
      const totalCompletedAchievements = games.totalCompletedAchievements;
      const totalPossibleAchievements = games.totalPossibleAchievements;

      numberOfGamesDiv.textContent = numberOfGames;
      totalPlaytimeDiv.textContent = formatHours(totalPlaytimeHours);
      averageCompletionOfGamesDiv.textContent = formatPercentage(achievementCompletionPercentage);

      // Account Value Data
      const accountValue = await getAccountValue(newsteamid);

      const accountMoneyValue = accountValue.accountValue;

      // ----------------------------------------------------------------------------------------

      const ageScore = await getAccountAgeScore(accountAgeSeconds / 360); //
      const gamesScore = await getAccountGamesScore(numberOfGames); //
      const bansScore = await getAccountBansScore(banNumber); //
      const playtimeScore = await getTotalPlaytimeScore(totalPlaytimeHours); //
      const last2WeeksScore = await getLast2WeeksScore(recentPlaytimeHours, (averageRecentPlaytime / 60)); //
      const valueScore = await getAccountValueScore(accountMoneyValue); //
      const friendsScore = await getAccountFriendsScore(friendTotal); //
      const achievementScore = await getAchievementPercentageScore(totalCompletedAchievements, totalPossibleAchievements); //

      updateSmurfBar(ageScore + gamesScore + bansScore + playtimeScore + last2WeeksScore + valueScore + friendsScore + achievementScore);

      // ----------------------------------------------------------------------------------------

        // Create a new recent search entry
        addRecentSearch(steamId, personaname, avatarFull);

    } catch (error) {
      console.error("Error fetching Steam profile:", error);
      messageDiv.textContent = "Error fetching Steam profile.";
      messageDiv.style.color = "red";
    }

    // Clear the input after processing
    searchInput.value = "";
  });
});