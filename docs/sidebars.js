/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  // tutorialSidebar: [{type: 'autogenerated', dirName: '.'}],

  // But you can create a sidebar manually
  docs: [
    {
      type: "category",
      label: "Introduction",
      link: {
        type: 'generated-index',
        title: 'Getting Started',
        slug: '/',
        keywords: ['Introduction'],
      },
      items: ["getting-started"],
    },
    {
      type: "category",
      label: "Contribution",
      link: {
        type: 'generated-index',
        title: 'Contribution',
        description: "Understand the server infastructure and scrapers to understand the intuitions behind the components behind FreeBooksAPI. It is not necessary to read this if you're just looking to use the API.",
        slug: '/contribution',
        keywords: ['contribution'],
      },
      items: ["contribution/overview", "contribution/intuitions"],
    },
    {
      type: "link",
      label: "API Reference",
      href: "https://freebooksapi.pyaesonemyo.me/api/latest/docs/",
    },
  ],
};

module.exports = sidebars;
