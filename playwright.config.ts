import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e_tests',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 1,
  workers: 1,
  reporter: [
    ['html', { outputFolder: 'e2e_tests/playwright-report', open: 'never' }],
    ['list'],
    ['junit', { outputFile: 'e2e_tests/artifacts/junit.xml' }],
  ],
  use: {
    baseURL: 'http://127.0.0.1:8000',
    trace: 'on-first-retry',
    screenshot: 'on',
    video: 'retain-on-failure',
    locale: 'ar',
    timezoneId: 'Asia/Riyadh',
  },
  outputDir: 'e2e_tests/artifacts/test-results',
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
