import { useState, useEffect } from 'react';

const PageControl = ({ totalPages = 1, onPageChange, jump = 1}) => {
  const [page, setPageState] = useState(0);

  const setPage = (newPage) => {
    const clamped = Math.max(0, Math.min(newPage, totalPages - 1));
    onPageChange(clamped);
  };

  const next = (currPage) => {
    console.log("Curr page is", currPage);
    setPage(currPage + 1);
  }

  const prev = (currPage) => setPage(currPage - 1);

  const nextJump = (currPage) => setPage(currPage + jump);
  const prevJump = (currPage) => setPage(currPage - jump);

  return {
    pageNum: page,
    setPage,
    prev,
    next,
    prevJump,
    nextJump
  };
};

export default PageControl;
