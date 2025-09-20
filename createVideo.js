import { execSync } from "child_process";

export function createVideo() {
  execSync(`ffmpeg -loop 1 -i assets/bg.jpg -i output/audio.mp3 -shortest -vf "scale=720:1280" -c:v libx264 -c:a aac -b:a 192k -pix_fmt yuv420p output/final.mp4`);
}

createVideo();