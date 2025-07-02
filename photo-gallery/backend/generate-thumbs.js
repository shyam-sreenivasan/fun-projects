// generate-thumbnails.js

import fs from 'fs';
import path from 'path';
import sharp from 'sharp';

// === CONFIG ===
const IMAGE_FOLDER = '/home/shyam/Pictures/appa-amma-60th'; // e.g. D:/Photos
const THUMB_FOLDER = path.join(IMAGE_FOLDER, 'thumbs');
const WIDTH = 300;
const HEIGHT = 300;

// === Ensure thumbs folder exists ===
if (!fs.existsSync(THUMB_FOLDER)) {
  fs.mkdirSync(THUMB_FOLDER);
}

// === Filter image files ===
const isImage = (file) => {
  const ext = path.extname(file).toLowerCase();
  return ['.jpg', '.jpeg', '.png', '.webp'].includes(ext);
};

// === Generate thumbnails ===
const generateThumbnails = async () => {
  const files = fs.readdirSync(IMAGE_FOLDER).filter(isImage);
  console.log(`Found ${files.length} image(s). Generating thumbnails...`);

  for (const file of files) {
    const inputPath = path.join(IMAGE_FOLDER, file);
    const outputPath = path.join(THUMB_FOLDER, file);

    if (!fs.existsSync(outputPath)) {
      try {
        await sharp(inputPath)
          .resize(WIDTH, HEIGHT, { fit: 'cover' }) // Crop to square
          .toFile(outputPath);
        console.log(`✅ Thumb created: ${file}`);
      } catch (err) {
        console.error(`❌ Failed for ${file}:`, err.message);
      }
    } else {
      console.log(`ℹ️ Thumb already exists: ${file}`);
    }
  }

  console.log('🎉 All thumbnails processed.');
};

generateThumbnails();
