// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'FreebooksAPI',
  tagline: 'A comprehensive (unofficial) API service for planet-ebooks, libgen/gen.lib.rus.ec, and libgen.lc.',
  url: 'https://freebooksapi.pyaesonemyo.dev',
  baseUrl: '/home/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.png',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'Rickaym', // Usually your GitHub org/user name.
  projectName: 'FreebooksAPI', // Usually your repo name.

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/Rickaym/FreeBooksAPI/tree/master/docs',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'FreebooksAPI',
        logo: {
          alt: 'FreebooksAPI logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'doc',
            docId: 'getting-started',
            position: 'left',
            label: 'Documentation',
          },
          {
            to: 'community',
            activeBasePath: 'community',
            position: 'left',
            label: 'Community',
          },
          {
            href: 'https://github.com/Rickaym/FreeBooksAPI',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Tutorial',
                to: '/docs/getting-started',
              },
              {
                label: 'API Reference',
                to: 'https://freebooksapi.pyaesonemyo.dev/api/latest/docs',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/Rickaym/FreeBooksAPI',
              },
              {
                label: 'Discord',
                href: 'https://discord.gg/UmnzdPgn6g',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Sponsor',
                to: 'https://www.buymeacoffee.com/rickaym',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} FreebooksAPI, Inc. Built with Docusaurus.`,
      },
      prism: {
        theme: darkCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
