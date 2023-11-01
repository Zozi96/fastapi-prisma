from prisma import Prisma

prisma = Prisma()

User = prisma.user
Task = prisma.task
