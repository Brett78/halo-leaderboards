from halo_leaderboards.taskapp.celery import app
from halo_leaderboards.leaderboards.halo_service import HaloService
from halo_leaderboards.leaderboards.models import Designation, Tier, Season, Playlist, Player, Rank


@app.task()
def populate_designations():
    service = HaloService()
    designations = service.get_designations()
    for designation in designations:
        name = designation.get('name')
        ref = designation.get('id')
        actual_designation = Designation(name=name, ref=ref)
        actual_designation.save()
        for tier in designation.get('tiers'):
            level = tier.get('id')
            image_url = tier.get('iconImageUrl')
            tier = Tier(level=level, image_url=image_url, designation=actual_designation)
            tier.save()

    return {'designation_count': Designation.objects.count(), 'tier_count': Tier.objects.count()}


@app.task()
def refresh_seasons():
    service = HaloService()
    seasons = service.get_seasons()
    for season in seasons:
        ref = season.get('id')
        name = season.get('name')
        start_date = season.get('startDate')
        end_date = season.get('endDate')
        is_active = season.get('isActive')
        actual_season = Season(name=name, ref=ref, start_date=start_date, end_date=end_date, is_active=is_active)
        actual_season.save()
        for playlist in season.get('playlists'):
            name = playlist.get('name')
            ref = playlist.get('id')
            playlist = Playlist(name=name, ref=ref, season=actual_season)
            playlist.save()

    return {'season_count': Season.objects.count(), 'playlist_count': Playlist.objects.count()}


@app.task()
def populate_leaderboards():
    service = HaloService()
    for season in Season.objects.all():
        for playlist in season.playlist_set.all():
            rankings = service.get_top_players(season.ref, playlist.ref)
            results = rankings.get('Results')
            for player in results:
                player_name = player.get('Player').get('Gamertag')
                actual_player, created = Player.objects.get_or_create(gamer_tag=player_name)
                score = player.get('Score')
                rank = score.get('Rank')
                csr = score.get('Csr')
                tier = score.get('Tier')
                designation_ref = score.get('DesignationId')
                designation = Designation.objects.get(ref=designation_ref)
                actual_tier = Tier.objects.get(designation=designation, level=tier)
                actual_rank = Rank(tier=actual_tier, player=actual_player, csr=csr, rank=rank, playlist=playlist,
                                   season=season)
                actual_rank.save()

    return {'player_count': Player.objects.count(), 'rank_count': Rank.objects.count()}


@app.task()
def refresh_active_season():
    service = HaloService()
    current_season = Season.objects.get(is_active=True, end_date=None)
    for playlist in current_season.playlist_set.all():
        rankings = service.get_top_players(current_season.ref, playlist.ref)
        results = rankings.get('Results')
        for player in results:
            player_name = player.get('Player').get('Gamertag')
            actual_player, created = Player.objects.get_or_create(gamer_tag=player_name)
            score = player.get('Score')
            rank = score.get('Rank')
            csr = score.get('Csr')
            tier = score.get('Tier')
            designation_ref = score.get('DesignationId')
            designation = Designation.objects.get(ref=designation_ref)
            actual_tier = Tier.objects.get(designation=designation, level=tier)

            # Could be current player or someone else
            try:
                existing_rank = Rank.objects.get(season=current_season, playlist=playlist, rank=rank)
                if existing_rank:
                    existing_rank.delete()
            except:
                pass

            # If it wasn't the current player, but they have a rank, just update it
            try:
                current_rank = Rank.objects.get(player=actual_player, season=current_season, playlist=playlist)
                if current_rank and current_rank.rank != rank:
                    current_rank.rank = rank
                    current_rank.save()
                    continue
            except:
                pass

            actual_rank = Rank(tier=actual_tier, player=actual_player, csr=csr, rank=rank, playlist=playlist,
                               season=current_season)
            actual_rank.save()

    return {'player_count': Player.objects.count(), 'rank_count': Rank.objects.count()}
