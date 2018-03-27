<template>
  <div id="app" class="container-fluid">
    <div class="container">
      <header>
        <h1 class="brand-font">A New York Times Machine</h1>
      </header>
    </div>
    <div class="container">
      <form method="get" class="mx-auto" v-on:submit.prevent>
        <div class="form-row" id="date-range">
          <div class="form-group form-group--inline col-md-4">
            <label for="start-date" class="sr-only">Beginning Date</label>
            <datepicker
              id="start-date"
              v-model="beginDate"
              placeholder="Choose Start Date"
              class="float-left"
            ></datepicker>
          </div>
          <div class="form-group form-group--inline col-md-4">
            <label for="end-date" class="sr-only">End Date</label>
            <datepicker
              id="end-date"
              v-model="endDate"
              placeholder="Choose End Date"
              class="float-left"
            ></datepicker>
          </div>
        </div>
        <div class="form-row" id="sort">
          <div class="form-group form-group--inline col-md-4">
            <label for="sort-order" class="sr-only">Sort by</label>
            <select class="float-left" v-model="sort">
              <option value="newest">Show Newest First</option>
              <option value="oldest">Show Oldest First</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group form-group--inline col-md-6">
            <div class="dropdown float-left"
            >
              <input
                type="text"
                name=""
                v-model="sectionSearch"
                class="float-left"
                placeholder="Search and select sections">
              <div
                class="dropdown-menu"
                :class="showMenu ? 'dropdown-menu--visible' : ''">
                <div
                  v-for="section in unselectedSections"
                  v-on:click.stop.prevent="selectedSections.push(section)"
                  class="menu-option"
                  :value="section"
                >{{section}}</div>
              </div>
            </div>
          </div>
          <div class="form-group form-group--inline col-md-6">
            <div
              v-for="selection in selectedSections"
              class="btn selection--remove"
              v-on:click="remove(selection)"
            >
              <label
                for="'remove_' + selection.replace(' ', '_')" class="sr-only"
              >Remove {{selection}}</label>
              <span :id="'remove_' + selection.replace(' ', '_')">{{selection}}</span>
              <i class="fas fa-times"></i>
            </div>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group form-group--inline col-md-6">
            <button
              type="submit"
              class="float-left btn btn-primary center"
              v-on:click="submit">Get Articles</button>
          </div>
        </div>
      </form>
    </div>
    <div class="container article-container">
      <div></div>
      <div v-for="article in articles" class="row article">
        <div class="col-md-4" v-if="getSmallestImage(article.multimedia)">
          <img
            :src="getSmallestImage(article.multimedia)"
            :href="article.web_url"
          >
        </div>
        <div v-else class="col-md-2"></div>
        <div class="col-md-8">
          <p><a :href="article.web_url" class="h3 a">{{article.headline.main}}</a></p>
          <p v-if="article.byline && article.byline.original">{{article.byline.original}}</p>
          <p>
            <time
              :datetime="article.pub_date.slice(0,10)"
            >{{formatDate(Date.parse(article.pub_date), 'D MMM YYYY')}}</time>
          </p>
        </div>
      </div>
    </div>
    <div class="container paginator">
      <div>
        <button v-on:click="getNewPage(-1)" :disabled="page === 0">Previous Page</button>
        <span>Page {{page + 1 }} of {{Math.ceil(articleCt / 10) }}</span>
        <button
          v-on:click="getNewPage(1)"
          :disabled="page === Math.ceil(articleCt / 10)"
        >Next Page</button>
      </div>
    </div>
    <footer class="container">
      <a href="https://github.com/ebbishop" class="brand brand-font anim-typewriter">A Bashirian-Bishop Project</a>
      <a href="https://github.com/ebbishop/timesmachine" class="fab fa-github fa-2x"></a>
      <a class="ny-times-attribution" href="http://developer.nytimes.com"></a>
    </footer>
  </div>
</template>

<script>
import moment from 'moment';
import Datepicker from 'vuejs-datepicker';
import axios from 'axios';
import sections from './sections';

export default {
  name: 'App',
  data() {
    return {
      sections,
      // user selections
      selectedSections: ['Dining & Wine', 'Dining and Wine', 'Food'],
      beginDate: null,
      endDate: null,
      page: 0,
      sort: 'newest',
      // articles
      articles: [],
      // section search
      sectionSearch: '',
      showMenu: true,
      // pagination
      articleCt: 0,
      // in-progress
      loading: false,
    };
  },
  components: {
    Datepicker,
  },
  computed: {
    unselectedSections() {
      return this.sections
        .filter(s => this.selectedSections.indexOf(s) === -1)
        .filter(s => s.toLowerCase().indexOf(this.sectionSearch.toLowerCase()) > -1);
    },
  },
  methods: {
    formatDate(date, format) {
      return moment(date).format(format);
    },
    getSmallestImage(array) {
      if (!array) return '';
      const medImage = array.find(item => item.subtype === 'wide');
      if (medImage) {
        return `https://nytimes.com/${medImage.url}`;
      }
      return '';
    },
    getNewPage(change) {
      this.page = this.page + change;
      const query = JSON.parse(JSON.stringify(this.$route.query)) || {};
      query.page = this.page + 1;
      this.$router.push({ query });
    },
    getArticles() {
      let selected = this.selectedSections.map(s => `"${s}"`).join(' ');
      selected = `section_name:(${selected})`;
      const params = {
        fq: selected,
        page: this.page,
        sort: this.sort,
      };
      if (this.beginDate) params.begin_date = this.formatDate(this.beginDate, 'YYYYMMDD');
      if (this.endDate) params.end_date = this.formatDate(this.endDate, 'YYYYMMDD');
      // section_name:("Food")
      axios.get('/get_articles', {
        params,
      })
        .then((res) => {
          this.articles = res.data.response.docs;
          this.articleCt = res.data.response.meta.hits;
          this.loading = false;
        });
    },
    remove(selection) {
      this.selectedSections.splice(this.selectedSections.indexOf(selection), 1);
    },
    submit() {
      const query = {};
      this.page = 0;
      if (this.beginDate) query.begin = this.formatDate(this.beginDate, 'YYYYMMDD');
      if (this.endDate) query.end = this.formatDate(this.endDate, 'YYYYMMDD');
      query.page = this.page + 1;
      query.sections = this.selectedSections.join(',');
      query.sort = this.sort;
      this.articles = [];
      this.loading = true;
      this.getArticles();
      this.$router.push({ query });
    },
  },
  mounted() {
    if (this.$route.query) {
      const query = this.$route.query;
      if (query.page) this.page = query.page - 1;
      if (query.sections) this.selectedSections = query.sections.split(',');
      if (query.sort) this.sort = query.sort;
      if (query.begin) this.beginDate = Date.parse(query.begin);
      if (query.end) this.endDate = Date.parse(query.end);
    }
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
form{
  border: 1px solid lightgray;
  border-radius: 5px;
  padding: 10px;
  max-width: 690px;
}
.form-group--inline > * {
  display: inline-block;
  vertical-align: top;
}
.dropdown > * {
  width: 85%;
}
.dropdown-menu{
  height: 100px;
  overflow: scroll;
}
.dropdown-menu--visible{
  display: inherit;
  position: inherit;
  z-index: 0;
}
.menu-option{
  padding-left: 5px;
}
.selection--remove {
    border: 1px solid lightgrey;
    margin: 2px;
    float: left;
}
.selection--remove svg {
  color: #71777a;
}
.article-container{
  margin-top: 30px;
}
.article{
  border-bottom: 1px solid lightgray;
  padding: 10px 0;
}
.article:first-child{
  padding-top: none;
}
.article:last-child{
  border-bottom: none;
  padding-bottom: none;
}
.paginator{
  padding-top: 10px;
  margin-bottom: 60px;
}
footer > a {
  color: inherit;
}
footer > a:hover{
  color: inherit;
}
.ny-times-attribution{
  background: url(http://static01.nytimes.com/packages/images/developer/logos/poweredby_nytimes_150c.png);
  width: 150px;
  display: inline-block;
  height: 30px;
  background-repeat: no-repeat;
}

.brand-font{
  font-family: 'Cutive Mono', monospace;
}

.brand{
    display: block;
    position: relative;
    top: 50%;
    right: 0;
    width: 15.8em;
    margin: 0 auto;
    font-size: 100%;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    transform: translateY(-50%);
}

/* Animation */
.anim-typewriter{
  animation: typewriter 4s steps(26) 1s 1 normal both;
}
@keyframes typewriter{
  from{width: 0;}
  to{width: 15.8em;}
}
@keyframes blinkTextCursor{
  from{border-right-color: rgba(0,0,0,.75);}
  to{border-right-color: transparent;}
}
</style>
