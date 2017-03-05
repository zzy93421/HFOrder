DELETE FROM menu_list;
INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (1, '创建工单', NULL, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (2, '专题工单', NULL, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (3, '常用工具', NULL, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (4, '工单任务', NULL, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (101, '创建实施文档', 1, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (102, '创建单组高频库程序', 1, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (103, '创建全组高频库程序', 1, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (104, '创建高频归集库程序', 1, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (105, '创建计奖验证库程序', 1, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (106, '创建数据库设计文档', 1, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (107, '创建单元测试报告', 1, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (201, '高频促销工单', 2, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (202, '调整高频游戏时间模板', 2, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (203, 'UMP查询模块', 2, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (301, '回退版本', 3, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (302, '批量替换', 3, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (303, '文档替换', 3, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (304, '导入EXCEL数据到表', 3, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (305, '从表导出EXCEL文件', 3, 'not define');

COMMIT;
