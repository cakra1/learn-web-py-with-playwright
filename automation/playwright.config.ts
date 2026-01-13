import { defineConfig } from '@playwright/test';

export default defineConfig({
  timeout: 60_000,

  use: {
    headless: false,

    // bikin semua aksi pelan
    launchOptions: {
      slowMo: 300, // 0.7 detik tiap aksi
    },

    // JANGAN TUTUP BROWSER LANGSUNG
    actionTimeout: 10_000,
  },
});
