<template>
  <div id="app">
    <header>
      <h1>A New York Times Machine</h1>
    </header>
    <section v-for="article in articles">
      <a :href="article.web_url">{{article.headline.main}}</a>
      <span>{{article.byline.original}}</span>
      <span><time :datetime="article.pub_date.slice(0,10)">{{formatDate(article.pub_date)}}</time></span>
    </section>
    <div>
      <button v-on:click="getNewPage(-1)" :disabled="page === 0">Previous</button>
      <span>Current page: {{page + 1 }}</span>
      <button v-on:click="getNewPage(1)">Next</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import sections from './sections';
import Datepicker from 'vuejs-datepicker';

export default {
  name: 'App',
  data() {
    return {
      sections,
      activeSections: ['Food'],
      startDate: null,
      endDate: null,
      page: 0,
      articles: [],
    };
  },
  components: {
    Datepicker
  },
  methods: {
    formatDate(dateString) {
      let shortString = dateString.slice(0,10);
      let year = shortString.slice(0,4);
      let month = shortString.slice(5,7);
      let day = shortString.slice(8,10);
      return month + '-' + day + '-' + year;
    },
    getNewPage(change) {
      this.page = this.page + change;
      this.getArticles();
    },
    getArticles() {
      axios.get('https://api.nytimes.com/svc/search/v2/articlesearch.json', {
        params: {
          'api-key': '93ac857a87c0496497514e971c96cf10',
          fq: 'section_name:("Food")',
          page: this.page,
      },
      })
      .then((res) => {
        console.log(res);
        this.articles = res.data.response.docs;
      });
    }
  },
  mounted() {
    this.getArticles();
  },
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
