DELETE FROM menu_list;

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (1, '��������', NULL);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (2, 'ר�⹤��', NULL);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (3, '���ù���', NULL);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (4, '��������', NULL);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (101, '����ʵʩ�ĵ�', 1);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (102, '���������Ƶ�����', 1);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (103, '����ȫ���Ƶ�����', 1);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (104, '������Ƶ�鼯�����', 1);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (105, '�����ƽ���֤�����', 1);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (106, '�������ݿ�����ĵ�', 1);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (107, '������Ԫ���Ա���', 1);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (201, '��Ƶ��������', 2);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (202, '������Ƶ��Ϸʱ��ģ��', 2);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (203, 'UMP��ѯģ��', 2);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (301, '���˰汾', 3);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (302, '�����滻', 3);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (303, '�ĵ��滻', 3);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (304, '����EXCEL���ݵ���', 3);

INSERT INTO menu_list
  (id, NAME, parent_id)
VALUES
  (305, '�ӱ���EXCEL�ļ�', 3);

COMMIT;
