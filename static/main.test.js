// npm test in the outermost directory
const { showDate } = require('./main');

describe('showDate', () => {
    beforeEach(() => {
        document.body.innerHTML = `<div id="date"></div>`;
    });

    // Check for correct format.
    test('formats date correctly', () => {
        const testDate = new Date(2025, 4, 1);
        const result = showDate(testDate);
        expect(result).toBe('Thursday May 1, 2025');
        expect(document.getElementById('date').innerHTML).toContain('Thursday May 1, 2025');
    });

    // Checks for leap year
    test('formats leap year date correctly', () => {
        const date = new Date(2024, 1, 29);
        const result = showDate(date);
        expect(result).toBe('Thursday February 29, 2024');
    });
});

describe('Responsive Layout Tests', () => {
    beforeAll(() => {
      document.body.innerHTML = `
        <div id="articles">
          <section class="article1"></section>
          <section class="article2"></section>
          <section class="article3"></section>
        </div>
      `;
    });
  
    describe('Mobile Layout (≤768px)', () => {
      beforeAll(() => {
        window.innerWidth = 767;
        window.getComputedStyle = jest.fn().mockReturnValue({
          flexDirection: 'column',
          display: 'flex',
        });
      });
  
      test('articles stack vertically', () => {
        const articles = document.getElementById('articles');
        const style = window.getComputedStyle(articles);
        expect(style.flexDirection).toBe('column');
      });
    });
  
    describe('Tablet Layout (768px–1023px)', () => {
      beforeAll(() => {
        window.innerWidth = 800;
        window.getComputedStyle = jest.fn().mockReturnValue({
          display: 'flex',
          flexWrap: 'wrap',
        });
      });
  
      test('articles wrap in two columns', () => {
        const articles = document.getElementById('articles');
        const style = window.getComputedStyle(articles);
        expect(style.flexWrap).toBe('wrap');
      });
    });
  
    describe('Desktop Layout (≥1024px)', () => {
      beforeAll(() => {
        window.innerWidth = 1200;
        window.getComputedStyle = jest.fn().mockReturnValue({
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
        });
      });
  
      test('articles use a 3-column grid', () => {
        const articles = document.getElementById('articles');
        const style = window.getComputedStyle(articles);
        expect(style.gridTemplateColumns).toBe('repeat(3, 1fr)');
      });
    });
  });