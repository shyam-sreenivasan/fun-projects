import React, { useEffect, useRef, useState } from 'react';
import axios from 'axios';
import {
  Grid,
  Dialog,
  DialogContent,
  IconButton,
  Box,
  Card,
  CardMedia,
  Typography,
  Container,
  Button,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import Paginator from './paging/Paginator';

const PAGE_SIZE = 24;
const BACKEND_IP = import.meta.env.VITE_BACKEND_IP || 'localhost';
const BASE_URL = `http://${BACKEND_IP}:5000`;

function App() {
  const [images, setImages] = useState([]);
  const [currPage, setCurrPage] = useState(0);
  const [total, setTotal] = useState(0);
  const [open, setOpen] = useState(false);
  const [selectedIdx, setSelectedIdx] = useState(null);
  const [slideshowActive, setSlideshowActive] = useState(false);

  const slideshowIntervalRef = useRef(null);

  // Fetch images for current page
  const fetchImages = (page) => {
    axios
      .get(`${BASE_URL}/api/images?page=${page}&size=${PAGE_SIZE}`)
      .then((res) => {
        setImages(res.data.images);
        setTotal(res.data.total);
        window.scrollTo({ top: 0, behavior: 'smooth' }); // scroll to top
      })
      .catch((err) => console.error('Failed to fetch images', err));
  };

  useEffect(() => {
    fetchImages(currPage);
  }, [currPage]);

  // Slideshow logic
  useEffect(() => {
    if (slideshowActive) {
      slideshowIntervalRef.current = setInterval(() => {
        setSelectedIdx((prevIdx) => {
          if (prevIdx === null || prevIdx >= images.length - 1) {
            clearInterval(slideshowIntervalRef.current);
            setSlideshowActive(false);
            setOpen(false);
            return prevIdx;
          }
          return prevIdx + 1;
        });
      }, 3000);
    }

    return () => {
      clearInterval(slideshowIntervalRef.current);
    };
  }, [slideshowActive, images]);

  const totalPages = Math.ceil(total / PAGE_SIZE);

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(to right, #c9d6ff, #e2e2e2)',
        py: 4,
      }}
    >
      <Container sx={{ width: '100vw', marginTop: '100px' }} maxWidth={false}>
        {/* Heading */}
        <Typography
          variant="h4"
          align="center"
          gutterBottom
          sx={{
            fontWeight: 'bold',
            color: '#333',
            mb: 4,
            textShadow: '1px 1px 2px rgba(0,0,0,0.1)',
          }}
        >
          Photo Gallery
        </Typography>

        {/* Slideshow Button */}
        <Box textAlign="center" mb={2}>
          <Button
            variant="contained"
            onClick={() => {
              if (images.length > 0) {
                setSelectedIdx(0);
                setOpen(true);
                setSlideshowActive(true);
              }
            }}
            disabled={slideshowActive}
          >
            Start Slideshow
          </Button>
        </Box>

        {/* Grid of images */}
        <Grid container spacing={2} justifyContent="center" alignItems="center">
          {images.map((img, idx) => (
            <Grid item xs={12} sm={6} md={4} key={idx}>
              <Card
                sx={{
                  width: '100%',
                  maxWidth: 300,
                  height: 300,
                  margin: 'auto',
                  cursor: 'pointer',
                  overflow: 'hidden',
                  borderRadius: 2,
                  boxShadow: 3,
                  '&:hover': {
                    transform: 'scale(1.02)',
                    transition: 'transform 0.2s ease-in-out',
                  },
                }}
                onClick={() => {
                  setSelectedIdx(idx);
                  setOpen(true);
                }}
              >
                <CardMedia
                  component="img"
                  image={img.thumbUrl}
                  alt={img.name}
                  sx={{
                    width: '100%',
                    height: '85%',
                    objectFit: 'cover',
                  }}
                />
                <Box sx={{ p: 1 }}>
                  <Typography variant="body2" align="center" sx={{ fontWeight: '500' }}>
                    {img.name}
                  </Typography>
                </Box>
              </Card>
            </Grid>
          ))}
        </Grid>

        {/* Pagination */}
        <Box sx={{ mt: 4 }}>
          <Paginator
            page={currPage}
            totalPages={totalPages}
            totalDataRows={total}
            currDataRows={images.length}
            onPageChange={setCurrPage}
            pageWidth={4}
          />
        </Box>

        {/* Lightbox Dialog */}
        <Dialog
          open={open}
          onClose={() => {
            setOpen(false);
            setSelectedIdx(null);
            setSlideshowActive(false);
            clearInterval(slideshowIntervalRef.current);
          }}
          maxWidth="md"
        >
          <DialogContent sx={{ p: 0, position: 'relative', bgcolor: 'black' }}>
            <IconButton
              onClick={() => {
                setOpen(false);
                setSelectedIdx(null);
                setSlideshowActive(false);
                clearInterval(slideshowIntervalRef.current);
              }}
              sx={{
                position: 'absolute',
                top: 16,
                right: 16,
                zIndex: 10,
                color: 'white',
                backgroundColor: 'rgba(0,0,0,0.5)',
                '&:hover': {
                  backgroundColor: 'rgba(0,0,0,0.7)',
                },
              }}
            >
              <CloseIcon />
            </IconButton>

            {/* Prev Button */}
            <IconButton
              onClick={() =>
                setSelectedIdx((prev) => (prev > 0 ? prev - 1 : prev))
              }
              sx={{
                position: 'absolute',
                top: '50%',
                left: 8,
                transform: 'translateY(-50%)',
                color: 'white',
                backgroundColor: 'rgba(0,0,0,0.5)',
                zIndex: 10,
                '&:hover': {
                  backgroundColor: 'rgba(0,0,0,0.7)',
                },
              }}
              disabled={selectedIdx === 0}
            >
              <NavigateBeforeIcon fontSize="large" />
            </IconButton>

            {/* Next Button */}
            <IconButton
              onClick={() =>
                setSelectedIdx((prev) => (prev < images.length - 1 ? prev + 1 : prev))
              }
              sx={{
                position: 'absolute',
                top: '50%',
                right: 8,
                transform: 'translateY(-50%)',
                color: 'white',
                backgroundColor: 'rgba(0,0,0,0.5)',
                zIndex: 10,
                '&:hover': {
                  backgroundColor: 'rgba(0,0,0,0.7)',
                },
              }}
              disabled={selectedIdx >= images.length - 1}
            >
              <NavigateNextIcon fontSize="large" />
            </IconButton>

            {/* Image Display */}
            <Box
              component="img"
              src={selectedIdx !== null ? images[selectedIdx].fullUrl : ''}
              alt="Preview"
              sx={{
                width: '100%',
                maxHeight: '80vh',
                objectFit: 'contain',
                display: 'block',
                margin: 'auto',
              }}
            />
          </DialogContent>
        </Dialog>
      </Container>
    </Box>
  );
}

export default App;
