<template>
  <div class="article-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>文章列表</span>
          <el-button type="primary" @click="createArticle">新建文章</el-button>
        </div>
      </template>

      <el-table :data="articles" style="width: 100%">
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="author" label="作者" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250">
          <template #default="scope">
            <el-button size="small" @click="editArticle(scope.row)">编辑</el-button>
            <el-button 
              size="small" 
              type="success" 
              @click="publishArticle(scope.row)"
              :disabled="scope.row.status === 'published'"
            >发布</el-button>
            <el-button 
              size="small" 
              type="danger" 
              @click="deleteArticle(scope.row)"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'ArticleList',
  setup() {
    const router = useRouter()
    const articles = ref([])

    const fetchArticles = async () => {
      try {
        const response = await axios.get('/articles')
        articles.value = response.data
      } catch (error) {
        ElMessage.error('获取文章列表失败')
      }
    }

    const createArticle = () => {
      router.push('/article/edit')
    }

    const editArticle = (article) => {
      router.push(`/article/edit/${article.id}`)
    }

    const publishArticle = async (article) => {
      try {
        await axios.post(`/articles/${article.id}/publish`)
        ElMessage.success('发布成功')
        fetchArticles()
      } catch (error) {
        ElMessage.error('发布失败')
      }
    }

    const deleteArticle = async (article) => {
      try {
        await ElMessageBox.confirm('确定要删除这篇文章吗？', '提示', {
          type: 'warning'
        })
        await axios.delete(`/articles/${article.id}`)
        ElMessage.success('删除成功')
        fetchArticles()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除失败')
        }
      }
    }

    const getStatusType = (status) => {
      const types = {
        draft: 'info',
        scheduled: 'warning',
        published: 'success',
        failed: 'danger'
      }
      return types[status] || 'info'
    }

    const getStatusText = (status) => {
      const texts = {
        0: '草稿',
        1: '待发布',
        2: '已发布',
        3: '发布失败'
      }
      return texts[status] || status
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleString()
    }

    onMounted(() => {
      fetchArticles()
    })

    return {
      articles,
      createArticle,
      editArticle,
      publishArticle,
      deleteArticle,
      getStatusType,
      getStatusText,
      formatDate
    }
  }
}
</script>

<style scoped>
.article-list {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 