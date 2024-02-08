import asyncio
from datetime import date

from sqlalchemy import and_, delete, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.providers.models import Provider, Tag, ProviderTag
from app.dao.base import BaseDAO
from app.database import async_session_maker

from app.logger import logger


class ProviderDAO(BaseDAO):
    model = Provider

    @classmethod
    async def get_providers(cls):
        '''
        SELECT providers.id, providers.name, providers.foundation_date,
        providers.registration_date,
        providers.rating, providers.verified, providers.location,
        providers.image_id, string_agg(tags.name, ', ') as tags
        FROM providers
        JOIN providers_tags ON providers.id = providers_tags.provider_id
        JOIN tags ON tags.id = providers_tags.tag_id
        GROUP BY providers.id;
        '''
        async with async_session_maker() as session:
            stmt = (
                select(Provider.id, Provider.name, Provider.foundation_date,
                       Provider.registration_date, Provider.rating,
                       Provider.verified, Provider.location,
                       Provider.image_id,
                       func.aggregate_strings(Tag.name, ', ').label('tags'))
                .select_from(Provider)
                .join(ProviderTag, Provider.id == ProviderTag.provider_id)
                .join(Tag, Tag.id == ProviderTag.tag_id)
                .group_by(Provider.id)
            )
            result = await session.execute(stmt)
            return result.mappings().all()

    @classmethod
    async def get_provider_by_id(cls, provider_id: int):
        '''
        WITH s_tags as (
            SELECT string_agg(tags.name, ', ')
            FROM providers
            JOIN providers_tags ON providers.id = providers_tags.provider_id
            JOIN tags ON tags.id = providers_tags.tag_id
            WHERE providers.id = 1)
        SELECT  providers.id, providers.name, providers.foundation_date, providers.registration_date,
        providers.rating, providers.verified, providers.location, s_tags
        providers.image_id
        FROM providers, s_tags
        WHERE providers.id = 1;
        '''
        async with async_session_maker() as session:
            tags = (
                select(
                    func.aggregate_strings(Tag.name, ', ').label('tags')
                )
                .select_from(Provider)
                .join(ProviderTag, Provider.id == ProviderTag.provider_id)
                .join(Tag, Tag.id == ProviderTag.tag_id)
                .where(Provider.id == provider_id)
                .cte(name="tags")
            )

            query = (
                select(Provider.id, Provider.name, Provider.foundation_date,
                       Provider.registration_date, Provider.rating,
                       Provider.verified, Provider.location,
                       Provider.image_id, tags)
                .select_from(Provider, tags)
                .where(Provider.id == provider_id)
            )

            result = await session.execute(query)
            result = result.mappings().one_or_none()
            return result

    @classmethod
    async def add_provider(cls,
                           name,
                           foundation_date,
                           registration_date,
                           rating,
                           verified,
                           location,
                           image_id,
                           tags
                           ):
        '''
        DO $$
        DECLARE new_user_id integer;
        DECLARE new_tag_id integer;
        BEGIN

        INSERT INTO providers (name, foundation_date, registration_date, rating, verified, location, image_id)
        VALUES ('ABC', '2020-01-01', '2021-01-01', 5, True, 'Moscow', 1)
        RETURNING id INTO new_user_id;

        INSERT INTO tags (name)
        VALUES ('Technology')
        RETURNING id INTO new_tag_id;

        INSERT INTO providers_tags (provider_id, tag_id)
        VALUES (new_user_id, new_tag_id);
        END $$;
        '''
        async with async_session_maker() as session:
            stmt_provider_id = (
                insert(Provider)
                .values(
                    name=name,
                    foundation_date=foundation_date,
                    registration_date=registration_date,
                    rating=rating,
                    verified=verified,
                    location=location,
                    image_id=image_id
                )
                .returning(Provider.id)
            )
            provider_id = await session.execute(stmt_provider_id)
            provider_id = int((provider_id.mappings().one_or_none()).id)

            stmt_tag_ids = (
                insert(Tag)
                .values(tags)
                .returning(Tag.id)
            )

            tag_ids = await session.execute(stmt_tag_ids)
            tag_ids = tag_ids.mappings().all()
            values = [{"tag_id": i['id'], "provider_id": provider_id}
                      for i in tag_ids]

            stmt = (
                insert(ProviderTag)
                .values(values)
                .returning(ProviderTag.provider_id, ProviderTag.tag_id)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.mappings()

    @classmethod
    async def del_provider(cls, provider_id: int):

        async with async_session_maker() as session:
            stmt = delete(ProviderTag).filter_by(provider_id=provider_id)
            await session.execute(stmt)
            stmt = delete(Provider).filter_by(id=provider_id)
            await session.execute(stmt)
            await session.commit()
