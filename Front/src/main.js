import { Telegraf, session, Markup } from 'telegraf'
import config from 'config'
import { message } from 'telegraf/filters'
import { ogg } from './ogg.js'
import { openai } from './openai.js'
import { code } from 'telegraf/format'
import csvtojson from 'csvtojson'

console.log(config.get('TEST_ENV'))

const INITIAL_SESSION = {
  messages: [],
}

const bot = new Telegraf(config.get('TELEGRAM_TOKEN'))

bot.use(session())

bot.command('new', async (ctx) => {
  ctx.session = INITIAL_SESSION
  await ctx.reply('Жду вашего голосового или текстового сообщения.')
})

bot.command('start', async (ctx) => {
    ctx.session = INITIAL_SESSION
    await ctx.reply('Жду вашего голосового или текстового сообщения.')
  })

bot.command('models', async (ctx) => {
    ctx.session ??= INITIAL_SESSION
    const options = {
      reply_markup: JSON.stringify({
        inline_keyboard: [
          [{ text: 'TF-IDF', callback_data: 'tf' }],
          [{ text: 'BOWords', callback_data: 'bow' }],
          [{ text: 'Word2Vec', callback_data: 'w2v' }],
          [{ text: 'DistilBERT', callback_data: 'db' }],
        ],
      })
    }
    await ctx.reply('Выберите модель:', options);
    const keyboard = Markup.keyboard([
        ['TF-IDF', 'BOWords'],
        ['Word2Vec', 'DistilBERT']
      ]).resize()

    await ctx.reply('Выберите опцию:', keyboard)
  })

bot.hears('TF-IDF', async (ctx) => {
  try {
    await ctx.reply('Вы выбрали TF-IDF')
    const csvData = await readCSV('./bd/tfidf.csv')
    const formattedData = formatCSVData(csvData)
    await ctx.reply('Результаты TF-IDF модели:')
    await ctx.reply(formattedData)
  } catch {
    console.log(`Error while TF-IDF`, e.message)
  }})

bot.hears('BOWords', async (ctx) => {
  try {
    await ctx.reply('Вы выбрали BOWords')
    const csvData = await readCSV('./bd/bowords.csv')
    const formattedData = formatCSVData(csvData)
    await ctx.reply('Результаты BOWords модели:')
    await ctx.reply(formattedData)
  } catch {
    console.log(`Error while BOWords`, e.message)
  }})

bot.hears('Word2Vec', async (ctx) => {
  try {
    await ctx.reply('Вы выбрали Word2Vec')
    const csvData = await readCSV('./bd/word2vec.csv')
    const formattedData = formatCSVData(csvData)
    await ctx.reply('Результаты Word2Vec модели:')
    await ctx.reply(formattedData)
  } catch {
    console.log(`Error while Word2Vec`, e.message)
  }})

bot.hears('DistilBERT', async (ctx) => {
  try {
    await ctx.reply('Вы выбрали DistilBERT')
    const csvData = await readCSV('./bd/distilbert.csv')
    const formattedData = formatCSVData(csvData)
    await ctx.reply('Результаты DistilBERT модели:')
    await ctx.reply(formattedData)
  } catch {
    console.log(`Error while DistilBERT`, e.message)
  }})

bot.action('bow', async (ctx) => {
  try {
    await ctx.answerCbQuery('Вы выбрали BOWords')
    const csvData = await readCSV('./bd/bowords.csv')
    const formattedData = formatCSVData(csvData)
    await ctx.reply('Результаты BOWords модели:')
    await ctx.reply(formattedData)
  } catch {
    console.log(`Error while bow`, e.message)
  }})

bot.action('w2v', async (ctx) => {
  try {
    await ctx.answerCbQuery('Вы выбрали Word2Vec')
    const csvData = await readCSV('./bd/word2vec.csv')
    const formattedData = formatCSVData(csvData)
    await ctx.reply('Результаты Word2Vec модели:')
    await ctx.reply(formattedData)
  } catch {
    console.log(`Error while w2v`, e.message)
  }})

bot.action('db', async (ctx) => {
  try {
    await ctx.answerCbQuery('Вы выбрали DistilBERT')
    const csvData = await readCSV('./bd/distilbert.csv')
    const formattedData = formatCSVData(csvData)
    await ctx.reply('Результаты DistilBERT модели:')
    await ctx.reply(formattedData)
  } catch {
    console.log(`Error while db`, e.message)
  }})

bot.action('tf', async (ctx) => {
  try {
    await ctx.answerCbQuery('Вы выбрали TF-IDF')
    const csvData = await readCSV('./bd/tfidf.csv')
    const formattedData = formatCSVData(csvData)
    await ctx.reply('Результаты TF-IDF модели:')
    await ctx.reply(formattedData)
  } catch {
    console.log(`Error while tf`, e.message)
  }})

async function readCSV(filePath) {
  try {
    const jsonArray = await csvtojson().fromFile(filePath);
    return jsonArray;
  } catch {
    console.log(`Error while readCSV`, e.message)
  }}

function formatCSVData(data) {
    let formattedData = ''
    try {
    data.forEach((item) => {
      const similarity = parseFloat(item.similarity).toFixed(4)
      formattedData += `Вакансия: ${item.name}\n`
      formattedData += `Ссылка: ${item.alternate_url}\n`
      formattedData += `Схожесть: ${similarity}\n`
      formattedData += `Резюме: ${item.tittle_resume}\n`
      formattedData += `Ссылка: ${item.resume_url}\n\n`
    })
    } catch {
      console.log(`Error while formatCSVData`, e.message)
    }
    return formattedData
  }

bot.on(message('voice'), async ctx => {
    ctx.session ??= INITIAL_SESSION
    if (ctx.from.id === config.get('YOUR_USER_ID') && ctx.chat.type === config.get('TYPE') && config.get('TEST_ENV') === "prod") {
    try {
      await ctx.reply(code('Сообщение принято.\nОжидаем ответ от сервера.'))
      const link = await ctx.telegram.getFileLink(ctx.message.voice.file_id)
      const userId = String(ctx.message.from.id)
      const oggPath = await ogg.create(link.href, userId)
      const mp3Path = await ogg.toMp3(oggPath, userId)
      const text = await openai.transcription(mp3Path)
      await ctx.reply(code(`Ваш запрос: ${text}`))
      ctx.session.messages.push({role: openai.roles.USER , content: text})
      const response = await openai.chat(ctx.session.messages)
      ctx.session.messages.push({
        role: openai.roles.ASSISTANT,
        content: response.content
    })
      await ctx.reply(response.content)
    } catch {
      console.log(`Error  while voice message`, e.message)
    }
  } else {
    await ctx.reply('Вам доступены только следующие команды: \n/start \n/new \n/models')
  }
})

bot.on('text', async (ctx) => {
    ctx.session ??= INITIAL_SESSION
    const messageText = ctx.message.text
    if (messageText.startsWith('/')) {
      const command = messageText.slice(1)
      if (!isCommandExist(command)) {
        await ctx.reply('Ошибка: Неверная команда.')
        return
      }
    }
    else {
        if (ctx.from.id === config.get('YOUR_USER_ID') && ctx.chat.type === config.get('TYPE') && config.get('TEST_ENV') === "prod") {
          try {
            await ctx.reply(code('Сообщение принято.\nОжидаем ответ от сервера.'))
            ctx.session.messages.push({
              role: openai.roles.USER,
              content: ctx.message.text
          })
            const response = await openai.chat(ctx.session.messages)
            ctx.session.messages.push({
              role: openai.roles.ASSISTANT,
              content: response.content
          })
            await ctx.reply(response.content)
          } catch {
            console.log(`Error while text message`, e.message)
          }
        } else {
          await ctx.reply('Вам доступены только следующие команды: \n/start \n/new \n/models')
        }
      }
    })

function isCommandExist(command) {
    const availableCommands = ['new', 'start', 'models']
    return availableCommands.includes(command)
  }

bot.launch()

process.once('SIGINT', () => bot.stop('SIGINT'))
process.once('SIGTERM', () => bot.stop('SIGTERM'))