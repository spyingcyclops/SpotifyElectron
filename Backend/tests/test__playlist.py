from datetime import datetime

from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
)
from test_API.api_test_artist import create_artist, delete_artist
from test_API.api_test_playlist import (
    create_playlist,
    delete_playlist,
    get_playlist,
    get_playlists,
    update_playlist,
)
from test_API.api_token import get_user_jwt_header


@fixture(scope="module", autouse=True)
def set_up(trigger_app_start):
    pass


def test_get_playlist_correct():
    name = "8232392323623823723"
    foto = "https://foto"
    descripcion = "hola"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    formatting = "%Y-%m-%dT%H:%M:%S"
    post_date_iso8601 = datetime.strptime(
        datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), formatting
    )

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=owner, password=password)

    res_create_playlist = create_playlist(
        name=name, descripcion=descripcion, foto=foto, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_get_playlist = get_playlist(name=name, headers=jwt_headers)
    assert res_get_playlist.status_code == HTTP_200_OK
    assert res_get_playlist.json()["name"] == name
    assert res_get_playlist.json()["photo"] == foto
    assert res_get_playlist.json()["description"] == descripcion
    assert res_get_playlist.json()["owner"] == owner

    try:
        fecha = res_get_playlist.json()["upload_date"]
        response_date = datetime.strptime(fecha, formatting)

        assert response_date.hour == post_date_iso8601.hour

    except ValueError:
        assert False

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_artist(owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_playlist_not_found():
    name = "8232392323623823723"

    foto = "https://foto"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=owner, password=password)

    res_get_playlist = get_playlist(name=name, headers=jwt_headers)
    assert res_get_playlist.status_code == HTTP_404_NOT_FOUND

    res_create_artist = delete_artist(owner)
    assert res_create_artist.status_code == HTTP_202_ACCEPTED


def test_post_playlist_correct():
    name = "8232392323623823723"
    foto = "https://foto"
    descripcion = "hola"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=owner, password=password)

    res_create_playlist = create_playlist(
        name=name, descripcion=descripcion, foto=foto, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_artist(owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_delete_playlist_correct():
    name = "8232392323623823723"
    foto = "https://foto"
    descripcion = "hola"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=owner, password=password)

    res_create_playlist = create_playlist(
        name=name, descripcion=descripcion, foto=foto, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_artist(owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_delete__playlist_not_found():
    name = "8232392323623823723"

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == HTTP_404_NOT_FOUND


def test_delete_playlist_invalid_name():
    name = ""

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == HTTP_405_METHOD_NOT_ALLOWED


def test_update_playlist_correct():
    name = "8232392323623823723"
    foto = "foto"
    descripcion = "descripcion"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=owner, password=password)

    res_create_playlist = create_playlist(
        name=name, descripcion=descripcion, foto=foto, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    new_description = "nuevadescripcion"

    res_update_playlist = update_playlist(
        name=name, foto=foto, descripcion=new_description, headers=jwt_headers
    )
    assert res_update_playlist.status_code == HTTP_204_NO_CONTENT

    res_get_playlist = get_playlist(name=name, headers=jwt_headers)
    assert res_get_playlist.status_code == HTTP_200_OK
    assert res_get_playlist.json()["description"] == new_description

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_artist(owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_update_playlist_correct_nuevo_nombre():
    name = "8232392323623823723"
    foto = "foto"
    descripcion = "descripcion"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=owner, password=password)

    res_create_playlist = create_playlist(
        name=name, descripcion=descripcion, foto=foto, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    new_name = "82323923236238237237"
    new_description = "nuevadescripcion"

    res_update_playlist = update_playlist(
        name=name,
        foto=foto,
        descripcion=new_description,
        nuevo_nombre=new_name,
        headers=jwt_headers,
    )
    assert res_update_playlist.status_code == HTTP_204_NO_CONTENT

    res_get_playlist = get_playlist(new_name, headers=jwt_headers)
    assert res_get_playlist.status_code == HTTP_200_OK

    res_delete_playlist = delete_playlist(new_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_artist(owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_playlists():
    name = "8232392323623823723"
    foto = "foto"
    descripcion = "descripcion"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=owner, password=password)

    res_create_playlist = create_playlist(
        name=name, descripcion=descripcion, foto=foto, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    new_name = "82323923236238237237"
    foto = "foto"
    descripcion = "descripcion"

    res_create_playlist = create_playlist(
        name=new_name, descripcion=descripcion, foto=foto, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_get_playlists = get_playlists(f"{name},{new_name}", headers=jwt_headers)
    assert res_get_playlists.status_code == HTTP_200_OK
    assert len(res_get_playlists.json()["playlists"]) == 2

    res_delete_playlist = delete_playlist(name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_playlist = delete_playlist(new_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_artist(owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


# TODO test playlist comprobar interior canciones
