import path from "path";
import sound from "sound-play";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ALERT_SOUND_FILENAME = "rip-and-tear.mp3";
const ALERT_SOUND_FILEPATH = path.join(__dirname, ALERT_SOUND_FILENAME);

let soundPlaying = false;
export async function playSoundAlert() {
  if (!soundPlaying) {
    try {
      soundPlaying = true;
      await sound.play(ALERT_SOUND_FILEPATH);
      soundPlaying = false;
    } catch (error) {
      console.log("Error playing sound alert.");
    }
  }
}
