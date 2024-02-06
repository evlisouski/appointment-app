import asyncio
from datetime import date

from sqlalchemy import and_, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.providers.models import Providers, Tags, ProvidersTags
from app.dao.base import BaseDAO
from app.database import async_session_maker

from app.logger import logger


class ProviderDAO(BaseDAO):
    model = Providers

    @classmethod
    async def get_provider_by_id(cls, provider_id: int):
        '''
        WITH s_tags as (
            SELECT string_agg(tags.name, ', ')
            FROM providers
            JOIN providers_tags ON providers.id = providers_tags.provider_id
            JOIN tags ON tags.id = providers_tags.tag_id
            WHERE providers.id = 1)
        SELECT providers.name, s_tags
        FROM providers, s_tags
        WHERE providers.id = 1;
        '''
        async with async_session_maker() as session:
            tags = (
                select(
                    func.aggregate_strings(Tags.name, ', ')
                )
                .select_from(Providers)
                .join(ProvidersTags, Providers.id == ProvidersTags.provider_id)
                .join(Tags, Tags.id == ProvidersTags.tag_id)
                .where(Providers.id == provider_id)
                .cte("s_tags")
            )

            query = (
                select(Providers.name, tags)
                .select_from(Providers, tags)
                .where(Providers.id == provider_id)
            )

            result = await session.execute(query)
            result = result.all()
            return result
