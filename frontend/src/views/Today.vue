<template>
  <div>
    <NewUserNotification :name="userName" :isVisible="isNotificationVisible" @hide="isNotificationVisible = false" />
    <Question :question="poll" class="mb-6"/>
    <CommentSection :comments="comments" :question_id="poll.id"/>
  </div>
</template>

<script>
import Question from '../components/Question.vue';
import CommentSection from '../components/CommentSection.vue';
import NewUserNotification from '../components/NewUserNotification.vue';
import apiClient from '../api.js';
import eventBus from '../utils/eventBus.js';
import { getCookie, setCookie, removeCookie } from '../utils/cookies';

export default {
  name: 'Today',
  components: {
    Question,
    CommentSection,
    NewUserNotification
  },
  data() {
    return {
      poll: {},
      comments: [],
      userName: '',
      isNotificationVisible: false,
    };
  },
  mounted() {
    eventBus.on('newUserCreated', this.showNotification);
  },
  beforeUnmount() {
    eventBus.off('newUserCreated', this.showNotification);
  },
  methods: {
    async fetchData() {
      const currentUserExists = !!getCookie('current_user')?.username;

      try {
        const todayDiscussion = await apiClient.get('/discussion');
        console.log(todayDiscussion.data);
        this.poll = todayDiscussion.data.question;
        this.comments = todayDiscussion.data.comments;
      } catch (error) {
        console.error('Error fetching data:', error);
      }

      if (!currentUserExists && getCookie('current_user')) {
        eventBus.emit('newUserCreated', getCookie('current_user').username);
      }
    },
    showNotification(name) {
      this.userName = name;
      this.isNotificationVisible = true;
      setTimeout(() => {
        this.isNotificationVisible = false;
      }, 10000); // Уведомление исчезает через 3 секунды
    },
  },
  created() {
    this.fetchData();
  },
}
</script>
