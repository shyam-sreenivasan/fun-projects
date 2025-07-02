// index.js
import express from 'express';
import cors from 'cors';
import fs from 'fs';
import path from 'path';
import sharp from 'sharp';

const app = express();
const PORT = 5000;

// 🔧 CONFIG
const IMAGE_DIR = process.argv[2];
if (!IMAGE_DIR) {
  console.error('❌ Please provide an image folder path as an argument.');
  process.exit(1);
}
const THUMB_DIR = path.join(IMAGE_DIR, 'thumbs');
const PAGE_SIZE_DEFAULT = 6;

// Enable CORS for frontend requests
app.use(cors());

// Serve full images and thumbnails statically
app.use('/images', express.static(IMAGE_DIR));
app.use('/thumbs', express.static(THUMB_DIR));

// Utility to filter valid image files
const isImageFile = (file) =>
  /\.(jpe?g|png|webp|bmp|gif)$/i.test(file);

// API to get paginated image list
app.get('/api/images', async (req, res) => {
  try {
    const page = parseInt(req.query.page || '0');
    const size = parseInt(req.query.size || PAGE_SIZE_DEFAULT);
    const files = fs.readdirSync(IMAGE_DIR)
      .filter((file) => isImageFile(file));

    const total = files.length;
    const start = page * size;
    const end = start + size;
    const paginatedFiles = files.slice(start, end);

    const images = paginatedFiles.map((file) => {
      const thumbPath = path.join(THUMB_DIR, file);
      const baseUrl = `${req.protocol}://${req.headers.host}`;

      return {
        name: file,
        thumbUrl: `${baseUrl}/thumbs/${file}`,
        fullUrl: `${baseUrl}/images/${file}`,
      };
    });

    res.json({ total, images });
  } catch (err) {
    console.error('Failed to read images:', err);
    res.status(500).json({ error: 'Server error while reading images' });
  }
});

// 🧠 Optional: endpoint to (re)generate thumbnails
app.get('/api/generate-thumbs', async (req, res) => {
  try {
    if (!fs.existsSync(THUMB_DIR)) {
      fs.mkdirSync(THUMB_DIR);
    }

    const files = fs.readdirSync(IMAGE_DIR)
      .filter((file) => isImageFile(file));

    for (const file of files) {
      const originalPath = path.join(IMAGE_DIR, file);
      const thumbPath = path.join(THUMB_DIR, file);

      // Skip if thumbnail already exists
      if (fs.existsSync(thumbPath)) continue;

      await sharp(originalPath)
        .resize(300, 300, { fit: 'cover' })
        .toFile(thumbPath);
    }

    res.json({ message: 'Thumbnails generated successfully' });
  } catch (err) {
    console.error('Thumbnail generation error:', err);
    res.status(500).json({ error: 'Failed to generate thumbnails' });
  }
});

// Start the server on 0.0.0.0 to be accessible over LAN
app.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ Server running at http://0.0.0.0:${PORT}`);
});
