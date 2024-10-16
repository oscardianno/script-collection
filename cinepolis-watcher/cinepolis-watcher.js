import axios from "axios";
import * as cheerio from "cheerio";
import fs from "fs";
import { playSoundAlert } from "./sound-alert.js";

// Configuration
const BASE_URL = "https://cinepolisentraalmasalla.com";
const LOGIN_URL = `${BASE_URL}/promo/login`;
const GAMES_URL = `${BASE_URL}/promo/dashboard/dinamicas/entra-al-mas-alla`;
const CHECK_INTERVAL = 2 * 60 * 1000; // 2 minutes
const STORAGE_FILE = "game_count.json";

// Authentication details: load from login.json file
const loginDetails = JSON.parse(fs.readFileSync("login.json", "utf8"));
const { USERNAME, PASSWORD } = loginDetails;

let lastGameCount = 0;

const axiosInstance = axios.create({
  headers: {
    "User-Agent":
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
    Accept:
      "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    Connection: "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
  },
  maxRedirects: 0,
  validateStatus: (status) => status >= 200 && status < 400,
});

async function login() {
  // First, get the login page to retrieve the token and set initial cookies
  const loginPageResponse = await axiosInstance.get(LOGIN_URL);
  const $ = cheerio.load(loginPageResponse.data);
  const token = $('input[name="_token"]').val();

  // Extract cookies from the login page response
  const cookies = loginPageResponse.headers["set-cookie"];
  if (!cookies) {
    throw new Error("No initial cookies received");
  }

  // Prepare the cookie string for the next request
  const cookieString = cookies.map((cookie) => cookie.split(";")[0]).join("; ");
  // console.log("DEBUG: Initial cookies:", cookieString);

  // Now, make the login request with the token and cookies
  const loginResponse = await axiosInstance.post(
    LOGIN_URL,
    new URLSearchParams({
      _token: token,
      email: USERNAME,
      password: PASSWORD,
      remember: "on",
    }).toString(),
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Cookie: cookieString,
        Referer: LOGIN_URL,
        Origin: BASE_URL,
        "Alt-Used": new URL(BASE_URL).hostname,
      },
    }
  );
  // console.log("DEBUG: Login response status:", loginResponse.status);
  // console.log("DEBUG: Login response headers:", loginResponse.headers);

  // Update cookies with any new ones from the login response
  const newCookies = loginResponse.headers["set-cookie"];
  if (newCookies) {
    return (
      cookieString +
      "; " +
      newCookies.map((cookie) => cookie.split(";")[0]).join("; ")
    );
  }

  return cookieString;
}

async function checkWebsite(cookies) {
  const response = await axiosInstance.get(GAMES_URL, {
    headers: {
      Cookie: cookies,
      Referer: `${BASE_URL}/promo/dashboard/dinamicas/bienvenida`,
    },
  });
  // console.log("DEBUG: Check website response status:", response.status);
  // console.log("DEBUG: Check website response headers:", response.headers);
  const $ = cheerio.load(response.data);
  const gameCount = $("#games > div").length;

  // Log time of check and game count
  const date = new Date();
  console.log(`${date.toLocaleTimeString()} - Game count: ${gameCount}`);
  if (gameCount !== lastGameCount) {
    console.log(`Game count changed from ${lastGameCount} to ${gameCount}`);
    playSoundAlert();
    console.log("GOGOGOGO");

    lastGameCount = gameCount;
    saveGameCount(gameCount);
  }
}

function saveGameCount(count) {
  fs.writeFileSync(STORAGE_FILE, JSON.stringify({ count }));
}

function loadGameCount() {
  try {
    const data = fs.readFileSync(STORAGE_FILE, "utf8");
    const { count } = JSON.parse(data);
    lastGameCount = count;
  } catch (error) {
    console.log("No previous game count found. Starting fresh.");
  }
}

async function main() {
  loadGameCount();

  try {
    const cookies = await login();
    console.log("Login successful");
    await checkWebsite(cookies);

    setInterval(async () => {
      try {
        await checkWebsite(cookies);
      } catch (error) {
        console.error("Error checking website:", error.message);
      }
    }, CHECK_INTERVAL);
  } catch (error) {
    console.error("Login failed:", error.message);
  }
}

main().catch(console.error);
