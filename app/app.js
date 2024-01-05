const express = require('express');
const multer = require('multer');
const zlib = require('zlib');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

app.post('/extract', upload.single('file'), (req, res) => {
  const startTime = Date.now();

  try {
    const buffer = req.file.buffer;

    // Decompress the Gzip file
    const decompressedData = zlib.gunzipSync(buffer);

    const endTime = Date.now();
    const elapsedTime = endTime - startTime;

    console.log(`Extraction completed in ${elapsedTime} milliseconds.`);
  } catch (error) {
    console.error('Error during extraction:', error);
    res.status(500).send('Internal Server Error');
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
