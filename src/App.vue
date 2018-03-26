<template>
  <div id="app" class="container-fluid">
    <div class="container">
      <header>
        <h1>A New York Times Machine</h1>
      </header>
    </div>
    <div class="container">
      <form action="" method="get" class="" v-on:submit.prevent>
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
            <div class="dropdown"
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
                  :value="section"
                >{{section}}</div>
              </div>
            </div>
          </div>
          <div class="col-md-6">
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
            <button type="submit" class="float-left btn btn-primary center" v-on:click="submit">Get Articles</button>
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
            >{{formatDate(Date.parse(article.pub_date), 'MM/DD/YYYY')}}</time>
          </p>
        </div>
      </div>
    </div>
    <div class="container">
      <div>
        <button v-on:click="getNewPage(-1)" :disabled="page === 0">Previous Page</button>
        <span>{{page + 1 }} / {{Math.ceil(articleCt / 10) }}</span>
        <button v-on:click="getNewPage(1)">Next Page</button>
      </div>
    </div>
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
      // return array.reduce((prev, curr) => prev.width > curr.width ? prev : curr);
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
        'api-key': '93ac857a87c0496497514e971c96cf10',
        fq: selected,
        page: this.page,
        sort: this.sort,
      };
      if (this.beginDate) params.begin_date = this.formatDate(this.beginDate, 'YYYYMMDD');
      if (this.endDate) params.end_date = this.formatDate(this.endDate, 'YYYYMMDD');
      // section_name:("Food")
      axios.get('https://api.nytimes.com/svc/search/v2/articlesearch.json', {
        params,
      })
        .then((res) => {
          console.log(res.data.response.docs); // eslint-disable-line no-console
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
.selection--remove {
    border: 1px solid lightgrey;
    margin: 2px;
    float: left;
}
.selection--remove svg {
  color: #71777a;
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
</style>
